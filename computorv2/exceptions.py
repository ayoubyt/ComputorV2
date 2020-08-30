class ComputerV2Exception(Exception):
    def __init__(self, message) -> None:
        super().__init__("\033[91merror : \033[0m" + message)
