#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  run shellcheck on project
#
#  Copyright (c) Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#

from ToolBOSCore.Util import FastScript
from ToolBOSCore.Settings import ProcessEnv
import io
import subprocess
import logging


# We use the gcc-style error-reporting of shellcheck, since it is compact
# and we do not need to really parse the output.
# We always know which codes have been checked, because we pass them with
# --include.
# .shellcheckrc-files are ignored, so that people don't bypass the checks.
# The shell-dialect is fixed as "bash".
_shellcheckCmd = 'shellcheck --format=gcc --include=%s --norc --shell=bash %s'


def checkScript( scriptPath, codes, enable=None ):
    sout = io.StringIO()
    serr = io.StringIO()

    failed = False
    reportedIssues = []
    cmd = _shellcheckCmd % (codes, scriptPath)
    if enable:
        cmd = '%s --enable=%s' % (cmd, enable)
    try:
        ProcessEnv.requireCommand('shellcheck')
        FastScript.execProgram( cmd, stdout=sout, stderr=serr )
    except subprocess.CalledProcessError as e:
        if serr.getvalue() != '':  # We have a real error.
            logging.error( serr.getvalue() )
            raise e
        else:  # Just non-zero exit-status of shellcheck, i.e. issues found.
            reportedIssues = sout.getvalue().splitlines()
            failed = True
    except OSError as e:
        logging.error( e )
        logging.error( 'shellcheck is not installed or not in the PATH.')

    sout.close()
    serr.close()

    return failed, reportedIssues
