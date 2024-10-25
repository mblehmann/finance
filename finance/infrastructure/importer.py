import csv
from datetime import datetime
from typing import List

from finance.application.dto import TransactionDto
from finance.application.interface import TransactionImporterInterface


class ErsteBankCsvTransactionImporter(TransactionImporterInterface):

    def import_transactions(self, filename: str) -> List[TransactionDto]:
        transactions = []
        with open(filename, 'r') as csv_file:
            csv_file.readline()
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                reference = row[9]
                day = datetime.strptime(row[0], '%d.%m.%Y').date()
                source = row[1]
                amount = row[6].replace(',', '')
                notes = row[8]
                category = ''
                month = day.month
                comments = ''
                tag = ''
                ignore = False
                item = TransactionDto(
                    reference,
                    day.isoformat(),
                    source,
                    amount,
                    notes,
                    category,
                    str(month),
                    tag,
                    comments,
                    str(ignore)
                )
                transactions.append(item)
        return transactions
