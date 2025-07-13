import logging
from executors.utils import load_subnode_config
from executors.sftp_collector import run_sftp_collector
from executors.file_validator import run_file_validator
from flow.models import Flow

logger = logging.getLogger(__name__)

NODE_EXECUTION_MAP = {
    "SFTP Collector": run_sftp_collector,
    "File Validator": run_file_validator,
    # Add more node types here
}

def run_flow(flow_id):
    flow = Flow.objects.get(id=flow_id)
    logger.info(f"Running flow: {flow.name}")

    nodes = flow.nodes.all().order_by("order")  # if you have ordering

    for node in nodes:
        if not node.subnodes.exists():
            logger.warning(f"Skipping node {node.name}, no subnodes configured")
            continue

        subnode = node.subnodes.filter(is_active=True).first()
        if not subnode:
            logger.warning(f"No active subnode for node {node.name}")
            continue

        config = load_subnode_config(subnode)

        runner = NODE_EXECUTION_MAP.get(node.name)
        if runner:
            logger.info(f"Executing node: {node.name} with subnode: {subnode.name}")
            runner(config)
        else:
            logger.error(f"No execution function defined for node: {node.name}")
