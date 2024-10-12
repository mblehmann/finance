import csv
from datetime import datetime
from typing import List
from application.dto import TransactionDto
from application.interface import TransactionImporterInterface


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
                exclude = False
                item = TransactionDto(
                    reference,
                    day.isoformat(),
                    source,
                    amount,
                    notes,
                    category,
                    str(month),
                    comments,
                    tag,
                    str(exclude)
                )
                transactions.append(item)
        return transactions
