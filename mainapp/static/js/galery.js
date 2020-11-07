var galery = [];
var next_page = '/api/images/?limit=10&offset=0'

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Check if this cookie string begin with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
             }
         }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function renderGaleryItem(props) {
    return (
        React.createElement("span", null,
        React.createElement("a", {"download": props.image, "href": props.full_path},
            React.createElement("img", {className: "img-thumbnail", "src": props.mini_path, "alt": "mini"}, null)
        ),
        React.createElement("input", {className: "btn btn-outline-danger btn-sm", "name": "remove", "type": "button", "id": "remove-" + props.pk, "value": "X"}, null)
        )
    )
}

function renderGalery() {
    var render_galery = [];
    for (let i = 0; i < galery.length; i++) {
        render_galery.push(
            React.createElement(renderGaleryItem, {'full_path': galery[i]['image_path'],
                                                   'mini_path': galery[i]['image_mini_path'],
                                                   'iamge': galery[i]['image'],
                                                   'pk': galery[i]['id']})
        )
    }
    const element = React.createElement("div", null, render_galery);
    ReactDOM.render(element, document.getElementById("root"));
    $('input[name="remove"]').click(removeImage);
}

function loadGalery() {
    if (!next_page) {
        return
    }
    $.ajax({
        url: next_page,
        type: 'GET',
        success: function(response) {
            galery = galery.concat(response['results']);
            renderGalery();
            next_page = response['next'];
            if (next_page) {
                $('#next-btn').removeAttr('disabled');
            }
            else {
                $('#next-btn').prop('disabled', true);
            }
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function removeImage(e) {
    var id = e.target.id.split('-')[e.target.id.split('-').length - 1];
    $.ajax({
        beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                },
        url: '/api/images/?pk=' + id,
        type: 'DELETE',
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response);
            galery = galery.filter(item => parseInt(item['id']) !== parseInt(id) );
            renderGalery();
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function uploadImage(e) {
    var data = new FormData();
    for (let i = 0; i < $('#file-input')[0].files.length; i++) {
        data.append(i, $('#file-input')[0].files[i]);
    }
    data.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken').val());
    $.ajax({
        url: '/api/images/',
        type: 'POST',
        processData: false,
        contentType: false,
        data: data,
        success: function(response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
        }
    });
}

$(document).ready(function(){
    loadGalery();
    $('#upload-btn').click(uploadImage);
    $('#next-btn').click(loadGalery);
})
