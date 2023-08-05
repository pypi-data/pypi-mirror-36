###
# Copyright (c) 2002-2005, Jeremiah Fincher
# Copyright (c) 2009, James McCoy
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import random

from supybot.test import *
import supybot.conf as conf

_letters = 'abcdefghijklmnopqrstuvwxyz'
def random_string():
    return ''.join(random.choice(_letters) for _ in range(16))

class ConfigTestCase(ChannelPluginTestCase):
    # We add utilities so there's something in supybot.plugins.
    plugins = ('Config', 'User', 'Utilities')

    prefix1 = 'somethingElse!user@host1.tld'
    prefix2 = 'EvensomethingElse!user@host2.tld'
    prefix3 = 'Completely!Different@host3.tld__no_testcap__'

    def testGet(self):
        self.assertNotRegexp('config get supybot.reply', r'registry\.Group')
        self.assertResponse('config supybot.protocols.irc.throttleTime', '0.0')

    def testList(self):
        self.assertError('config list asldfkj')
        self.assertError('config list supybot.asdfkjsldf')
        self.assertNotError('config list supybot')
        self.assertNotError('config list supybot.replies')
        self.assertRegexp('config list supybot', r'@plugins.*@replies.*@reply')

    def testHelp(self):
        self.assertError('config help alsdkfj')
        self.assertError('config help supybot.alsdkfj')
        self.assertNotError('config help supybot') # We tell the user to list.
        self.assertNotError('config help supybot.plugins')
        self.assertNotError('config help supybot.replies.success')
        self.assertNotError('config help replies.success')

    def testHelpDoesNotAssertionError(self):
        self.assertNotRegexp('config help ' # Cont'd.
                             'supybot.commands.defaultPlugins.help',
                             'AssertionError')

    def testHelpExhaustively(self):
        L = conf.supybot.getValues(getChildren=True)
        for (name, v) in L:
            self.assertNotError('config help %s' % name)

    def testSearch(self):
        self.assertNotError('config search chars')
        self.assertNotError('config channel reply.whenAddressedBy.chars @')
        self.assertNotRegexp('config search chars', self.channel)

    def testDefault(self):
        self.assertNotError('config default '
                            'supybot.replies.genericNoCapability')

    def testConfigErrors(self):
        self.assertRegexp('config supybot.replies.', 'not a valid')
        self.assertRegexp('config supybot.repl', 'not a valid')
        self.assertRegexp('config supybot.reply.withNickPrefix 123',
                          'True or False.*, not \'123\'.')
        self.assertRegexp('config supybot.replies foo', 'settable')

    def testReadOnly(self):
        old_plugins_dirs = conf.supybot.directories.plugins()
        try:
            self.assertResponse('config supybot.commands.allowShell', 'True')
            self.assertNotError('config supybot.directories.plugins dir1')
            self.assertNotError('config supybot.commands.allowShell True')
            self.assertResponse('config supybot.commands.allowShell', 'True')
            self.assertResponse('config supybot.directories.plugins', 'dir1')

            self.assertNotError('config supybot.commands.allowShell False')
            self.assertResponse('config supybot.commands.allowShell', 'False')

            self.assertRegexp('config supybot.directories.plugins dir2',
                    'Error.*not writeable')
            self.assertResponse('config supybot.directories.plugins', 'dir1')
            self.assertRegexp('config supybot.commands.allowShell True',
                    'Error.*not writeable')
            self.assertResponse('config supybot.commands.allowShell', 'False')

            self.assertRegexp('config commands.allowShell True',
                    'Error.*not writeable')
            self.assertResponse('config supybot.commands.allowShell', 'False')

            self.assertRegexp('config COMMANDS.ALLOWSHELL True',
                    'Error.*not writeable')
            self.assertResponse('config supybot.commands.allowShell', 'False')
        finally:
            conf.supybot.commands.allowShell.setValue(True)
            conf.supybot.directories.plugins.setValue(old_plugins_dirs)

    def testOpEditable(self):
        var_name = 'testOpEditable' + random_string()
        conf.registerChannelValue(conf.supybot.plugins.Config, var_name,
                registry.Integer(0, 'help'))
        self.assertNotError('register bar passwd', frm=self.prefix3,
                private=True)
        self.assertRegexp('whoami', 'bar', frm=self.prefix3)
        ircdb.users.getUser('bar').addCapability(self.channel + ',op')

        self.assertRegexp('config plugins.Config.%s 1' % var_name,
                '^Completely: Error: ',
                frm=self.prefix3)
        self.assertResponse('config plugins.Config.%s' % var_name,
                'Global: 0; #test: 0')

        self.assertNotRegexp('config channel plugins.Config.%s 1' % var_name,
                '^Completely: Error: ',
                frm=self.prefix3)
        self.assertResponse('config plugins.Config.%s' % var_name,
                'Global: 0; #test: 1')

    def testOpNonEditable(self):
        var_name = 'testOpNonEditable' + random_string()
        conf.registerChannelValue(conf.supybot.plugins.Config, var_name,
                registry.Integer(0, 'help'), opSettable=False)
        self.assertNotError('register bar passwd', frm=self.prefix3,
                private=True)
        self.assertRegexp('whoami', 'bar', frm=self.prefix3)
        ircdb.users.getUser('bar').addCapability(self.channel + ',op')

        self.assertRegexp('config plugins.Config.%s 1' % var_name,
                '^Completely: Error: ',
                frm=self.prefix3)
        self.assertResponse('config plugins.Config.%s' % var_name,
                'Global: 0; #test: 0')

        self.assertRegexp('config channel plugins.Config.%s 1' % var_name,
                '^Completely: Error: ',
                frm=self.prefix3)
        self.assertResponse('config plugins.Config.%s' % var_name,
                'Global: 0; #test: 0')

        self.assertNotRegexp('config channel plugins.Config.%s 1' % var_name,
                '^Completely: Error: ')
        self.assertResponse('config plugins.Config.%s' % var_name,
                'Global: 0; #test: 1')

    def testChannel(self):
        self.assertResponse('config reply.whenAddressedBy.strings ^',
                'The operation succeeded.')
        self.assertResponse('config channel reply.whenAddressedBy.strings @',
                'The operation succeeded.')
        self.assertResponse('config channel reply.whenAddressedBy.strings', '@')
        self.assertNotError('config channel reply.whenAddressedBy.strings $')
        self.assertResponse('config channel #testchan1 reply.whenAddressedBy.strings', '^')
        self.assertResponse('config channel #testchan2 reply.whenAddressedBy.strings', '^')
        self.assertNotError('config channel #testchan1,#testchan2 reply.whenAddressedBy.strings .')
        self.assertResponse('config channel reply.whenAddressedBy.strings', '$')
        self.assertResponse('config channel #testchan1 reply.whenAddressedBy.strings', '.')
        self.assertResponse('config channel #testchan2 reply.whenAddressedBy.strings', '.')


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

