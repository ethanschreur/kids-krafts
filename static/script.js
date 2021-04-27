$('.table-row').click(function(evt) {
	let firstParent = $(evt.target).parent();
	let id = 0;
	if (typeof $(firstParent).data().id === 'number') {
		id = $(firstParent).data().id;
	} else {
		id = $(firstParent).parent().data().id;
	}
	if ($(firstParent).data().type === 'order') {
		window.location.href = `/orders/${id}`;
	} else {
		window.location.href = `/products/${id}`;
	}
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
	const id = $(evt.target).data().id;
	const amount = $(evt.target).val();
	if ($(evt.target).hasClass('amount-input')) {
		calcTotalCost();
	}
	axios.post('/cart/amount', { id, amount });
});

$('.date-check').change(function(evt) {
	$('.date-check').prop('checked', false);
	$(evt.target).prop('checked', true);
});

$('.checkout-button').click(async function(evt) {
	const dateTimes = document.querySelectorAll('.date-check');
	let count = 0;
	let selected = '';
	for (const opts of dateTimes) {
		if ($(opts).prop('checked')) {
			count++;
			selected = opts;
		}
	}
	if (count === 1) {
		const stripe = Stripe(
			'pk_test_51IjncDG7eCWHTgYHTQP30rZivUhfi0DagZW3FDTMmLD4enV4cRWnx8B6ftGWNEvFaiXUdPe5Md9LU4V4RHqo2cMq00byMZcJqY'
		);
		let month = '';
		if (parseInt(selected.id.substring(0, 2), 10) < 15) {
			month = $(selected).data().secondMonth;
		} else {
			month = $(selected).data().firstMonth;
		}
		const sessionId = await axios.post('/create-checkout-session', { pickup: selected.id, month });
		return stripe.redirectToCheckout({ sessionId: sessionId.data.id });
	}
});
