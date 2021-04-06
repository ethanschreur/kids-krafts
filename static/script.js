$('.table-row').click(function(evt) {
	let firstParent = $(evt.target).parent();
	let id = 0;
	if (typeof $(firstParent).data().id === 'number') {
		id = $(firstParent).data().id;
	} else {
		id = $(firstParent).parent().data().id;
	}
	window.location.href = `/products/${id}`;
});
