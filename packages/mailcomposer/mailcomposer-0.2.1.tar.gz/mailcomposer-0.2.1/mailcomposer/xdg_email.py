#!/usr/bin/env python

"""Fallback interface using xdg-email."""

# Note: This interface is intended for Unix, but technically it would also
# work on Windows if there was an equivalent xdg-email.exe utility.

import os
import sys
import subprocess

from .base import BaseMailComposer
from .exceptions import MailComposerError
from .util import find_executable


__all__ = ["XDGEmailComposer"]


# Find the xdg-email executable
xdg_email = find_executable("xdg-email")


class _XDGEmailComposer(BaseMailComposer):
    """Interface for xdg-email.

    This is provided as a fallback if no native mailcomposer interface
    exists for your preferred email client.

    The body_format property is not supported and will be silently ignored.
    Messages will always be composed using your client's default format.
    """

    def display(self, blocking=True):
        """Call xdg-email to display this message."""

        args = [xdg_email]

        # Process the message headers
        # Note: The "to" field is processed last
        for addr in self._cc:
            args.append("--cc")
            args.append(addr)
        for addr in self._bcc:
            args.append("--bcc")
            args.append(addr)
        if self._subject:
            args.append("--subject")
            args.append(self._subject)

        # Format the message body
        # xdg-email doesn't currently support specifying the body format
        if self._body:
            args.append("--body")
            args.append(self._body)

        # Process message attachments
        for path in self._attachments:
            args.append("--attach")
            args.append(path)

        # Add recipients last
        for addr in self._to:
            args.append(addr)

        # Display the message
        xdg_email_process = subprocess.Popen(args)
        if blocking:
            xdg_email_process.wait()


if xdg_email:
    XDGEmailComposer = _XDGEmailComposer

else:
    XDGEmailComposer = None
