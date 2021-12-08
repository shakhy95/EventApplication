function getAge(now, birth){
    var timeDiff = Math.abs(now - birth);
    return Math.floor(timeDiff / (1000*3600*24*365));
}

$(function() {
    $('#btn-filter').click( function() {

        var checked_gen = $('#checkbox_gen').is(":checked");
        var radio_gen = undefined;
        if(checked_gen){
            radio_gen = $("input[name='radio_gen']:checked").val();
            if (typeof radio_gen == 'undefined') {
                alert("You have not chosen a gender!!")
                return;
            }
        }

        var min_age = "", max_age = "";
        var checked_age = $('#checkbox_age').is(":checked");
        if(checked_age){
            min_age = $('#f_min_age').val();
            max_age = $('#f_max_age').val();
            if(min_age === "" && max_age === ""){
                alert("At least one of the age filter must be greater than 0!!");
                return;
            } else if((!(max_age === "") && (!(min_age === ""))) && max_age < min_age){
                alert("'Max Age' must be grater than 'Min Age'!!");
                return;
            }
        }

        if(!(checked_gen) && !(checked_age)){
            alert("No filter chosen!!");
            return;
        }

        $('#list-container > div').each( function(){
            var context = $(this);
            var id = context.attr('id');

            if(checked_gen){
                var gender = $("#"+id+"-gender").text();
                $('#gen-type').text(radio_gen);
                if(!(gender === radio_gen)){
                    context.hide();
                }
            }

            if(checked_age){
                var date = $("#"+id+"-date").text();
                var birth = new Date(date).getTime();
                var age = getAge(Date.now(), birth);
                //console.log(age);
                if(min_age > 0 && max_age > 0){
                    $('#min-age').text(min_age);
                    $('#max-age').text(max_age);
                    if((age < min_age) || (age > max_age)){
                        context.hide();
                    }
                } else if(min_age > 0){
                    $('#min-age').text(min_age);
                    if(age < min_age){
                        context.hide();
                    }
                } else {
                    $('#max-age').text(max_age);
                    if(age > max_age){
                        context.hide();
                    }
                }
            }
        })
        $('#filter-form')[0].reset();
        $('#filter-div').hide();
        $('#filter-info').show();
    });

    $('#btn-show').click( function() {
        $('#list-container > div').each( function(){
            var context = $(this);
            id = context.attr('id');
            context.show();
        })
        $('#filter-div').show();
        $('#filter-info').hide();
    });
})
