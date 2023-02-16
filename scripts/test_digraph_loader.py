"""Testing for DirectedGraphController class"""

import logging

from . import directed_graph


def setup_logging(log_file, log_level, process):
    """initializes a logger object with a common format"""
    log_level = getattr(
        logging, log_level.upper(), logging.INFO
    )  # set provided or set INFO
    msg_format = "%(asctime)s|%(name)s|[%(levelname)s]: %(message)s"
    logging.basicConfig(format=msg_format, datefmt="%m-%d %H:%M", level=log_level)
    log_handler = logging.FileHandler(log_file, mode="w")
    formatter = logging.Formatter(msg_format)
    log_handler.setFormatter(formatter)
    logger = logging.getLogger(
        f"{process}"
    )  # sets what will be printed for the log process
    logger.addHandler(log_handler)
    return logger


if __name__ == "__main__":
    my_graph = directed_graph.DirectedGraphController(
        setup_logging("./dscensor-digraph.log", "debug", "generate-digraph"),
        dscensor_nodes="./autocontent",
    )
    print(my_graph.dump_nodes())
    print(my_graph.dump_edges())
