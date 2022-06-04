// validation functions 
function isLatitude(lat) {
    return isFinite(lat) && Math.abs(lat) <= 90;
  }
  
  function isLongitude(lng) {
    return isFinite(lng) && Math.abs(lng) <= 180;
  }





/************************************/
// Event Listners 

$('#request_type').change((event)=>{
if( $('#request_type').prop('checked')){
    $('#term_section').css('display', 'none')
    $('#geolocation_section').css('display', 'flex')
}else {
    $('#term_section').css('display', 'flex')
    $('#geolocation_section').css('display', 'none')
}
})

/*******************************************/
const download = function (id){
    $('#div_'+id).empty()
    $.ajax({
        type: 'POST',
        url:  '/download/'+id,
        contentType: false,
        cache: false,
        processData: false
    }).done((xhr)=>{
        $('#div_'+id).append('<img src="../static/success.svg" width="30px"/>')
    }).fail((xhr)=>{
        $('#div_'+id).append('<img src="../static/error.svg" width="30px"/>')

    });
}
/*****************************************/


$('#geolocation_section').css('display', 'none')
var err = $('#error_msg');
var log = $('#log')
var alt = $('#alert');
var succ =$('#sucess')
var loading=$('#loader')
var btn=$('#sender')
log.css('display', 'none')
loading.css('display', 'none')
var request_type = $('#request_type').prop('checked') ;
function submit_data(){
    var error_message='';
    var is_err = false ;
    $("#display").empty();
    alt.addClass('hide');
    alt.removeClass('show');
    succ.addClass('hide');
    succ.removeClass('show');
    if($('#request_type').prop('checked')){
        var number_of_pages = $( "#nbr_1" ).val();
        var longitude = $("#longitude").val() ;
        var latitude = $("#latitude").val() ;
        var radius = $("#radius").val() ;
            if(!latitude || !isLatitude(latitude)){
            error_message = 'Please provide a valid Latitude <br>' + error_message;
            err.html(error_message);
            is_err=true;
            } 

            if(!longitude ||!isLongitude(longitude )){
            error_message = 'Please provide a valid Longitude <br>'+ error_message;
            err.html(error_message);
            is_err=true;
            } 
        
        if((longitude && !latitude) || (!longitude && latitude)) {
            error_message = 'Please provide both Longitude  and Latitude <br>'+ error_message;
            err.html(error_message);
            is_err=true;
        }
        if(is_err){
            log.css('display', 'block')
            alt.addClass('show');
            alt.removeClass('hide');
        
        }else{
            btn.css('display', 'none')
            btn.addClass('hide');
            btn.removeClass('show');
            loading.css('display', 'inline-block')
            loading.addClass('show');
            loading.removeClass('hide');
            var form_data = new FormData();
            form_data.append('NUMBER', number_of_pages);
            form_data.append('RADIUS', radius);
            form_data.append('LONG', longitude);
            form_data.append('LATI', latitude);
            $.ajax({
                type: 'POST',
                url:  '/get_pages_geo',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    loading.addClass('hide');
                    loading.removeClass('show');
                    loading.css('display', 'none')
                    log.css('display', 'block')
                    succ.addClass('show');
                    succ.removeClass('hide');
                    btn.css('display', 'inline-block')
                    btn.addClass('show');
                    btn.removeClass('hide');
                    
                        var clean_data = []
                        $('#display').append('<table id="tb" class="display table" width="100%"></table>')
                        data.map((row)=>{
                            clean_data.push([row.id,row.title,row.lon,row.lat,row.dist,'<span id="div_'+row.id+'" class="download"> <a  id="'+row.id+'"> <i class="bi bi-cloud-arrow-down"></i> </button> </span>'])
                        });
                        $('#tb').DataTable( {
                            data: clean_data,
                            columns: [
                                { title: "ID" },
                                { title: "TITLE" },
                                { title: "LONGTITUDE" },
                                { title: "LATITUDE" },
                                { title: "DISTANCE" },
                                { title: "DOWNLOAD" }
                            ]
                        } );
                          
                        data.map((row)=>{
                            $('#tb').on('click', '#'+row.id, function() {
                                download(row.id);
                              });
                            

                        })
                    
                },
                complete: function(xhr) {
                    if (xhr.status != 200) {
                        loading.css('display', 'none')
                        loading.addClass('hide');
                        loading.removeClass('show');
                        btn.addClass('show');
                        btn.removeClass('hide');
                        btn.css('display', 'inline-block')
                        if(xhr.status == 400) {
                            error_message = 'Connection  problem, Unable to scrap the data';
                        }
                        if(xhr.status == 500) {
                            error_message = 'API PROBLEM';
                        }
                        
                        err.html(error_message);
                        log.css('display', 'block')
                        alt.addClass('show');
                        alt.removeClass('hide');
                        
                        }
                } 
                });
            
            }

    }else{
        var number_of_pages = $( "#nbr_2" ).val();
        var term =  $( "#term" ).val(); 
        if ( term == "" || term == null) {
            error_message = 'Please provide the Term <br>'+ error_message;
            err.html(error_message);
            is_err=true;
        }
        if(is_err){
            log.css('display', 'block')
            alt.addClass('show');
            alt.removeClass('hide');
        
        }else{
            btn.css('display', 'none')
            btn.addClass('hide');
            btn.removeClass('show');
            loading.css('display', 'inline-block')
            loading.addClass('show');
            loading.removeClass('hide');
            var form_data = new FormData();
            form_data.append('NUMBER', number_of_pages);
            form_data.append('TERM', term);
            $.ajax({
                type: 'POST',
                url:  '/get_pages_term',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data, textStatus, xhr) {
                    loading.addClass('hide');
                    loading.removeClass('show');
                    loading.css('display', 'none')
                    log.css('display', 'block')
                    succ.addClass('show');
                    succ.removeClass('hide');
                    btn.css('display', 'inline-block')
                    btn.addClass('show');
                    btn.removeClass('hide');
                    
                        var clean_data = []
                        $('#display').append('<table id="tb" class="display table" width="100%"></table>')
                        data.map((row)=>{
                            clean_data.push([row.id,row.title,row.date,row.word_count,row.size,'<span  id="div_'+row.id+'" class="download"> <a id="'+row.id+'"> <i class="bi bi-cloud-arrow-down"></i> </button> </span>'])
                        });
                        $('#tb').DataTable( {
                            data: clean_data,
                            columns: [
                                { title: "ID" },
                                { title: "TITLE" },
                                { title: "DATE" },
                                { title: "WORD COUNT" },
                                { title: "SIZE" },
                                { title: "DOWNLOAD" }
                            ]
                        } );
                        
                        data.map((row)=>{
                            $('#tb').on('click', '#'+row.id, function() {
                                download(row.id);
                              });
                            

                        })
                    
                       
                    
                },
                complete: function(xhr) {
                    if (xhr.status != 200) {
                    
                    loading.addClass('hide');
                    loading.removeClass('show');
                    loading.css('display', 'none')
                    btn.addClass('show');
                    btn.removeClass('hide');
                    btn.css('display', 'inline-block')
                    if(xhr.status == 400) {
                        error_message = 'Connection  problem, Unable to scrap the data';
                    }
                    if(xhr.status == 500) {
                        error_message = 'API PROBLEM';
                    }
                    
                    err.html(error_message);
                    log.css('display', 'block')
                    alt.addClass('show');
                    alt.removeClass('hide');
                    }
                } 
                });
            
            }

    }
     
}
   
/**************************************** */


