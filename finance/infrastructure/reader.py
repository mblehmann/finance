from finance.application.interface import InputReaderInterface


class CmdInputReader(InputReaderInterface):

    def get_input(self, prompt: str) -> str:
        return input(prompt)
