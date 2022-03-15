import logging
from typing import Optional

from src.alerting.alert_utils.slack_bot_api import SlackBotApi
from src.alerting.alerts.alerts import Alert, ProblemWithSlackBot
from src.alerting.channels.channel import Channel, ChannelSet
from src.utils.redis_api import RedisApi


class SlackChannel(Channel):

    def __init__(self, channel_name: str, logger: logging.Logger,
                 redis: Optional[RedisApi], slack_bot: SlackBotApi,
                 backup_channels: ChannelSet) -> None:
        super().__init__(channel_name, logger, redis)

        self._slack_bot = slack_bot
        self._backup_channels = backup_channels
        self._space = ' ' if self.channel_name != '' else ''

    def _alert(self, alert: Alert, subject: str) -> None:
        if self._slack_bot is not None:
            slack_ret = self._slack_bot.send_message(
                '*{}*: `{}`'.format(subject, alert))
            self._logger.debug("alert: slack_ret: %s", slack_ret)
            if slack_ret['ok']:
                self._logger.info('Sent slack alert.')
            else:
                self._backup_channels.alert_error(
                    ProblemWithSlackBot(slack_ret['description']))
        else:
            self._logger.warning('Slack bot alerts are disabled.')

    def alert_info(self, alert: Alert) -> None:
        self._alert(alert=alert,
                    subject='INFO')

    def alert_minor(self, alert: Alert) -> None:
        self._alert(alert=alert,
                    subject='MINOR')

    def alert_major(self, alert: Alert) -> None:
        self._alert(alert=alert,
                    subject='MAJOR')

    def alert_error(self, alert: Alert) -> None:
        self._alert(alert=alert,
                    subject='ERROR')
