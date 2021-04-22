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

function calcTotalCost() {
	let total = 0;
	for (let row of $('#your_cart_tbody').children()) {
		const amount = $(row).children()[2].firstElementChild.value;
		const price = $($(row).children()[2].firstElementChild).data().price;
		total += parseFloat(amount) * parseFloat(price);
	}
	total = total.toFixed(2);
	$('#total_cost').empty();
	$('#total_cost').append(total);
}

$('.add-to-cart').click(async function(evt) {
	let firstParent = $(evt.target).parent();
	let id = 0;
	let name = '';
	let image = '';
	let price = '';
	// get cost and amount
	if ($(firstParent).data().sect === 'purchase_sect') {
		id = $(firstParent).data().id;
		name = $(firstParent).data().name;
		image = $(firstParent).data().image;
		price = $(firstParent).data().price;
	} else {
		id = $($(firstParent).parent()).data().id;
		name = $($(firstParent).parent()).data().name;
		image = $($(firstParent).parent()).data().image;
		price = $($(firstParent).parent()).data().price;
	}
	let prod = { id, name, image, price };
	await axios.post('/cart', prod);
	if ($($(`.add-${id}`)[0]).hasClass('btn-primary')) {
		$($(`.add-${id}`)[0]).addClass('btn-success');
		$($(`.add-${id}`)[0].firstElementChild).remove();
		$($(`.add-${id}`)[0]).prepend('<i class="fas fa-check"></i>');
	}
});

$('#your_cart_tbody').click(function(evt) {
	let secondParent = $(evt.target).parent().parent();
	if ($(evt.target).hasClass('remove-from-cart')) {
		let id = 0;
		if (secondParent.data().id) {
			id = secondParent.data().id;
			secondParent.remove();
		} else {
			id = $(secondParent).parent().data().id;
			$(secondParent).parent().remove();
		}
		axios.post('/cart/remove', { id });
		calcTotalCost();
	}
});

$('#your_cart_tbody').change(function(evt) {
	if ($(evt.target).hasClass('amount-input')) {
		calcTotalCost();
	}
});

$('.date-check').change(function(evt) {
	$('.date-check').prop('checked', false);
	$(evt.target).prop('checked', true);
});
