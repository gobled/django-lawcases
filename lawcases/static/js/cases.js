function confirm_delete() {
	return confirm('Confirm delete action?');
}

function checkNotEmpty(elem, key) {
	console.log(jQuery(elem).val());
	if (jQuery(elem).val()) {
		jQuery('#' + key).removeClass('error');
		jQuery('#' + key + ' .help-inline').addClass('hidden').text('');
	}
}

function submitForm(elem, type) {
	$form = jQuery(elem).parents('#'+type+':first').find('form:first');
	
	jQuery.post($form.attr('action'), $form.serialize(), function(data) {
	
		data = jQuery.parseJSON(data);
		if (data.error) {
			message = jQuery.parseJSON(data.message);
			jQuery.each(message, function(key, val) {
				if (type == "modal"){
					jQuery('#group_' + key).addClass('error');
					jQuery('#group_' + key + ' .help-inline').removeClass('hidden').text(val[0]);
				}
				else{
					jQuery('[name=['+key+']').addClass('error');
					//jQuery('#' + key + '_err').removeClass('hidden').text(val[0]);
				}
			});
		} else {
			$('#'+type+':type').modal('hide');
			location.reload();
		}
	});
	return false;
}