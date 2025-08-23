import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from document_manager.models import DocumentNode

class Command(BaseCommand):
    help = 'Imports a structured document from a CSV file into DocumentNode.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')
        parser.add_argument(
            '--root_name',
            type=str,
            help='The name (item) for the root node of the imported document.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        root_name_override = options['root_name']
        self.stdout.write(self.style.SUCCESS(f"Starting import from {csv_file_path}..."))

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                rows = list(reader)
        except FileNotFoundError:
            raise CommandError(f"File not found at: {csv_file_path}")
        except Exception as e:
            raise CommandError(f"An error occurred reading the CSV file: {e}")

        created_nodes = {}
        rows_by_id = {row['id']: row for row in rows}

        def process_node(node_id):
            if node_id in created_nodes:
                return created_nodes[node_id]

            try:
                row_data = rows_by_id[node_id]
            except KeyError:
                self.stderr.write(self.style.ERROR(f"Error: Node with ID {node_id} is referenced as a parent but does not exist in the CSV."))
                return None

            parent_id = row_data['parent_id']
            claim_text = row_data['claim_text']
            item_text = ' '.join(claim_text.split()[:7]) + '...'

            new_node = None
            if parent_id == '0':
                root_item_name = root_name_override if root_name_override else item_text
                new_node = DocumentNode.add_root(
                    item=root_item_name,
                    text=claim_text,
                    node_type='document'
                )
                self.stdout.write(self.style.SUCCESS(f"Created root document: '{root_item_name}'"))
            else:
                parent_node = process_node(parent_id)
                if parent_node:
                    new_node = parent_node.add_child(
                        item=item_text,
                        text=claim_text,
                        node_type='paragraph'
                    )
                    self.stdout.write(f"  - Added child '{item_text}' to '{parent_node.item}'")

            if new_node:
                created_nodes[node_id] = new_node
            return new_node

        for row in rows:
            process_node(row['id'])

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully imported {len(created_nodes)} nodes from {csv_file_path}."))
