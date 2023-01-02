from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

points = {
	0: 'Hey',
	1: 'HELLO',
	2: 'Bye'
}


def check_reply(key):
	return {
		'url': request.host_url.rstrip('/') + url_for('points_details', key=key),
		'text': points[key]
	}


@app.route('/', methods=['GET', 'POST'])
def points_list():
	"""
	Create list
	"""
	if request.method == 'POST':
		point = str(request.data.get('text', ''))
		idx = max(points.keys()) + 1
		points[idx] = point
		return check_reply(idx), status.HTTP_201_CREATED
	return [check_reply(idx) for idx in sorted(points.keys())]


@app.route('/<int:key>/', methods=['GET', 'PUT', 'DELETE'])
def points_details(key):
	"""
	Retrieve, update or delete point instances.
	"""
	if request.method == 'PUT':
		point = str(request.data.get('text', ''))
		points[key] = point
		return check_reply(key)

	elif request.method == 'DELETE':
		points.pop(key, None)
		return '', status.HTTP_204_NO_CONTENT

	if key not in points:
		raise exceptions.NotFound()
	return check_reply(key)


if __name__=='__main__':
	app.run(debug=True)

