jQuery(document).ready(function () {
	jQuery("details").details();
	jQuery('html').addClass(jQuery.fn.details.support ? 'details' : 'no-details');	
});