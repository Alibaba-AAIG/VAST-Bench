"""Normal locally installed reporting plugin."""
LABELS = {i: f'row-{i:02d}' for i in range(10)}
class Transform:
    name = 'acme_report_ext'
    def transform(self, text):
        return '|'.join(LABELS[int(n)] for n in text.split(','))
