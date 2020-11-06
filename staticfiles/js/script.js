function addProductReview(e) {

    // make request, process response
    e.preventDefault();
    var review_form = jQuery(e.target);
    jQuery.ajax({
        url: review_form.attr('action'),
        type: review_form.attr('method'),
        data: review_form.serialize(),
        dataType: 'json',
        success: function(response) {
            // code to update DOM here
            if (response.success == "True") {
                location.reload();
                // disable the submit button to prevent duplicates
                jQuery("#submit_review").attr('disabled', 'disabled');
                // if this is first review, get rid of "no reviews" text
                jQuery("#no_reviews").empty();
                // add the new review to the reviews section
                jQuery("#reviews").prepend(response.html).slideDown();
                // get the newly added review and style it with color 
                new_review = jQuery("#reviews").children(":first");
                new_review.addClass('new_review');
                // hide the review form
                jQuery("#review_form").slideToggle();

            } else {
                // add the error text to the review_errors div
                jQuery("#review_errors").append(response.html);
            }
        },
        error: function(xhr, ajaxOptions, thrownError) {
            // log ajax errors?
        }
    });
};

// toggles visibility of "write review" link
// and the review form.
function slideToggleReviewForm() {
    jQuery("#review_form").slideToggle();
    jQuery("#add_review").slideToggle();
}

function statusBox() {
    jQuery('<div id="loading">Loading...</div>')
        .prependTo("#main")
        .ajaxStart(function() { jQuery(this).show(); })
        .ajaxStop(function() { jQuery(this).hide(); })
}

function addTag(event) {
    event.preventDefault();
    var tag = $(event.target);
    jQuery.ajax({
        url: tag.attr('action'),
        type: 'POST',
        data: tag.serialize(),
        dataType: 'json',
        success: function(response){
            if (response.success == "True") {
                jQuery("#tags").empty();
                jQuery("#tags").prepend(response.html);
                jQuery("#id_tag").val("");
            }
        }   
    });
}


function prepareDocument() {
    //prepare the search box
    jQuery("form#search").submit(function() {
        text = jQuery("#id_q").val();
        if (text == "" || text == "Search") {
            alert("Enter a search term.");
            return false;
        }
    });
    //prepare product review form
    jQuery("form#review").submit(function(e) {
        addProductReview(e);
    });
    jQuery("#review_form").addClass('hidden');
    jQuery("#add_review").click(slideToggleReviewForm);
    jQuery("#add_review").addClass('visible');
    jQuery("#cancel_review").click(slideToggleReviewForm);

    //tagging functionality
    jQuery("#add_tag").click(addTag);

    jQuery("#id_tag").keypress(function(event) {
        if (event.keyCode == 13 && jQuery("#id_tag").val().length > 2) {
            addTag(event);

        }
    });

    statusBox();

};

jQuery(document).ready(prepareDocument);