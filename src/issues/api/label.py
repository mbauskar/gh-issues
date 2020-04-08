from issues.models import Label

def get_or_create_labels(labels):
	""" check if labels exists, if not then create """
	def format_label(label):
		keys_to_keep = ['name', 'color']
		args = { key: label.get(key, '') for key in keys_to_keep }
		return Label(**args)

	labels_mapper = { label.get('name'): label for label in labels }

	avaiable_lables = list(Label.objects.filter(name__in=labels_mapper.keys()))
	avaiable_names = [label.name for label in avaiable_lables]

	to_create = [ format_label(labels_mapper.get(name)) \
		for name in labels_mapper.keys() if name not in avaiable_names ]

	if not to_create:
		return avaiable_lables

	created = Label.objects.bulk_create(to_create)
	avaiable_lables.extend(created)

	return avaiable_lables