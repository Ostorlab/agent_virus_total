"""VirusTotal agent implementation : Agent responsible for scanning a file through the Virus Total DB."""
import logging

from ostorlab.agent import agent
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent.mixins import agent_report_vulnerability_mixin
from ostorlab.agent import message as msg
from ostorlab.agent.kb import kb
from ostorlab.runtimes import definitions as runtime_definitions
from rich import logging as rich_logging

from agent import virustotal
from agent import process_scans


logging.basicConfig(
    format='%(message)s',
    datefmt='[%X]',
    handlers=[rich_logging.RichHandler(rich_tracebacks=True)],
    level='INFO',
    force=True
)
logger = logging.getLogger(__name__)


class VirusTotalAgent(agent.Agent, agent_report_vulnerability_mixin.AgentReportVulnMixin):
    """Agent responsible for scanning a file through the Virus Total DB."""

    def __init__(self, agent_definition: agent_definitions.AgentDefinition,
                 agent_settings: runtime_definitions.AgentSettings) -> None:
        """Init method.
        Args:
            agent_definition: Attributes of the agent.
            agent_settings: Settings of running instance of the agent.
        """
        super().__init__(agent_definition, agent_settings)
        self.api_key = self.args.get('api_key')

    def process(self, message: msg.Message) -> None:
        """Process message of type v3.asset.file. Scan the file content through the Virus Total public API, assign a
         risk rating, a technical report and emits a message of type v3.report.vulnerability .

        Args:
            message: Message containing the file to scan.

        Raises:
            VirusTotalApiError: In case the Virus Total api encountered problems.
            NameError: In case the scans were not defined.
        """
        logger.info('processing message of selector : %s', message.selector)
        logger.info('scanning the file with the Virustotal API.')
        response = virustotal.scan_file_from_message(message, self.api_key)

        try:
            scans = virustotal.get_scans(response)
        except virustotal.VirusTotalApiError:
            logger.error('virustotal API encountered some problems. Please try again.')
            raise

        technical_detail = process_scans.get_technical_details(scans)
        risk_rating = process_scans.get_risk_rating(scans)
        self.report_vulnerability(entry=kb.KB.VIRUSTOTAL_SCAN,
                                  technical_detail=technical_detail,
                                  risk_rating=risk_rating)


if __name__ == '__main__':
    logger.info('starting agent..')
    VirusTotalAgent.main()
