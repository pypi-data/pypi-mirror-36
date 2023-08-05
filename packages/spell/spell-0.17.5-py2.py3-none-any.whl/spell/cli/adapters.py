# -*- coding: utf-8 -*-
import click
from requests.adapters import HTTPAdapter

from spell.version import __version__ as CLI_VERSION


UPDATE_MESSAGE = ("Your Spell CLI version {} is below the minimum recommended version of {}. "
                  "Please upgrade by running `pip install --upgrade spell`")


class UpdateNoticeAdapter(HTTPAdapter):
    """Print a one-time notice if responses from the Spell API say there are CLI updates available."""

    def __init__(self, *args, **kwargs):
        super(UpdateNoticeAdapter, self).__init__(*args, **kwargs)
        self.printed_notice = False

    def add_headers(self, request, **kwargs):
        user_agent = request.headers.get("User-Agent", "")
        user_agent = "SpellCLI/{} {}".format(CLI_VERSION, user_agent).strip()
        request.headers["User-Agent"] = user_agent
        return super(UpdateNoticeAdapter, self).add_headers(request, **kwargs)

    def build_response(self, request, response):
        new_cli_version = response.headers.get("Spell-CLI-Update")
        if new_cli_version and not self.printed_notice:
            self.print_update_notice(new_cli_version)
        return super(UpdateNoticeAdapter, self).build_response(request, response)

    def print_update_notice(self, version):
        text = click.wrap_text(UPDATE_MESSAGE.format(CLI_VERSION, version),
                               initial_indent="✨ ", subsequent_indent="✨ ")
        click.echo(text, err=True)
        self.printed_notice = True
