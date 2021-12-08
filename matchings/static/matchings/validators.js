$(function() {
    $('#evt-button').click( function() {
        console.log("Event button clicked!");
        var alertstr = ""; 
        var title = $('#evt-title').val();
        if(title === ""){
            alertstr += "Missing : Title \n";
        }
        var desc = $('#evt-desc').val();
        if(desc === ""){
            alertstr += "Missing : Description \n";
        }
        var loc = $('#evt-loc').val();
        if(loc === ""){
            alertstr += "Missing : Location \n";
        }
        var date = $('#evt-date').val();
        if(date === ""){
            alertstr += "Missing : Date \n";
        }
        var time = $('#evt-time').val();
        if(time === ""){
            alertstr += "Missing : Time \n";
        }
        var type = $('input[name="evt-type"]:checked').val();
        console.log(type);
        if(typeof type == 'undefined'){
            alertstr += "Missing : Type \n";
        }
        if(!(alertstr === "")){
            alert(alertstr);
            return;
        }
        $('#evt-form').submit();
    });
})

function showCSSError(elem){
    elem.css({
        "border": "1px solid red",
        "background": "#FFCECE"
    });
}

function clearCSSError(elem){
    elem.css({
        "border": "",
        "background": ""
    });
}

function validateEmail(email) {
    if (email === '')
        return false;
    else if (!((email.indexOf('.') > 0) && (email.indexOf('@') > 0)) ||
    /[^a-zA-Z0-9.@_-]/.test(email))
        return false;
    return true;
}

function validateUsername(field) {
    if (field === ""){
        return false;
    } else if (/[^a-zA-Z0-9_-]/.test(field)){
        return false;
    } else{
        return true;
    }
}

function passwordMatch(passwd1, passwd2){
    if(passwd1 === "" || passwd2 === ""){
        return false;
    } else if (passwd1 === passwd2){
        return true;
    } else {
        return false;
    }
}

$(function() {
    $('#sign-username').change( function(){
        var text = $(this).val();
        if(!validateUsername(text)){
            showCSSError($(this));
        } else {
            clearCSSError($(this));
        }
    });
    $('#sign-email').change( function(){
        var text = $(this).val();
        if(!validateEmail(text)){
            showCSSError($(this));
        } else {
            clearCSSError($(this));
        }
    });
    $('#sign-conf-passwd').change( function(){
        var text1 = $(this).val();
        var text2 = $('#sign-passwd').val();
        if(!(passwordMatch(text1, text2))){
            showCSSError($(this));
            showCSSError($('#sign-passwd'));
        } else {
            clearCSSError($(this));
            clearCSSError($('#sign-passwd'));
        }
    });
    $('#sign-btn').click(function() {
        var username = $('#sign-username').val();
        var email = $('#sign-email').val();
        var pass1 = $('#sign-passwd').val(), pass2 = $('#sign-conf-passwd').val();
        var errmsg = "";
        if(!validateUsername(username)){
            errmsg += "Error : Username \n";
        }
        if(!validateEmail(email)){
            errmsg += "Error : Email \n";
        }
        if(!(passwordMatch(pass1, pass2))){
            errmsg += "Error : Password not matching \n";
        }
        if(!(errmsg === "")){
            alert(errmsg);
            return;
        }
        $('#sign-form').submit();
    });
})
