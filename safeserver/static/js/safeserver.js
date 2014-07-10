    this.tooltip = function(){

            xOffset = 10;
            yOffset = 20;

        $("img.tooltip").hover(function(e){
            this.t = this.title;
            this.title = "";
            $("body").append("<p id='tooltip'>"+ this.t +"</p>");
            $("#tooltip")
                .css("top",(e.pageY - xOffset) + "px")
                .css("left",(e.pageX + yOffset) + "px")
                .fadeIn("fast");
        },
        function(){
            this.title = this.t;
            $("#tooltip").remove();
        });
        $("img.tooltip").mousemove(function(e){
            $("#tooltip")
                .css("top",(e.pageY - xOffset) + "px")
                .css("left",(e.pageX + yOffset) + "px");
        });
    };

$( document ).ready(function() {

    tooltip();

    $('.banner').unslider({
        speed: 500,               //  The speed to animate each slide (in milliseconds)
        delay: 9000,              //  The delay between slide animations (in milliseconds)
        complete: function() {},  //  A function that gets called after every slide animation
        keys: true,               //  Enable keyboard (left, right) arrow shortcuts
        dots: true,               //  Display dot navigation
        fluid: false              //  Support responsive design. May break non-responsive designs
        });

    $(".rslides").responsiveSlides({
        auto: true,             // Boolean: Animate automatically, true or false
        speed: 500,            // Integer: Speed of the transition, in milliseconds
        timeout: 4000,          // Integer: Time between slide transitions, in milliseconds
        pager: false,           // Boolean: Show pager, true or false
        nav: false,             // Boolean: Show navigation, true or false
        random: false,          // Boolean: Randomize the order of the slides, true or false
        pause: false,           // Boolean: Pause on hover, true or false
        pauseControls: true,    // Boolean: Pause when hovering controls, true or false
        prevText: "Previous",   // String: Text for the "previous" button
        nextText: "Next",       // String: Text for the "next" button
        maxwidth: "",           // Integer: Max-width of the slideshow, in pixels
        navContainer: "",       // Selector: Where controls should be appended to, default is after the 'ul'
        manualControls: "",     // Selector: Declare custom pager navigation
        namespace: "rslides",   // String: Change the default namespace used
        before: function(){},   // Function: Before callback
        after: function(){}     // Function: After callback
        });

        $(function() {
            $("input").click(function(){
                var myCheckboxess = [];
                $("#mikoo input:checkbox:checked").map(function(){
                    myCheckboxess.push($(this).val());
                });

                var cena_ofert = $( "#starter_cena" ).val();

                $.ajax({
                    type: "GET",
                    url: '/ajax_starter/',
                    dataType: "json",
                    data : $("#dodatek_wlasny").serialize(),
                    success: function(data) {
                        var liczba ;
                        var dane = [];
                        var cena = [];
                        var html = [];
                        var html2 = [];
                        var cena_tyk = [];
                        var total = 0, count, ofirt;

                        $('#okiter').empty();
                        $('#cenkii').empty();

                           $.each(myCheckboxess, function(i) {
                                liczba = myCheckboxess[i];
                                    for(var k in data){
                                      if(data.hasOwnProperty(k) && data[k].pk == liczba)
                                         dane.push("<li value="+data[k].pk+">DODATEK: "+data[k].fields.nazwa+"</li>");
                                    }
                                    for(var m in data){
                                      if(data.hasOwnProperty(m) && data[m].pk == liczba)
                                         cena.push("<li value="+data[m].fields.cena_netto+">"+data[m].fields.cena_netto+" zł netto</li>");
                                    }
                                    for(var c in data){
                                      if(data.hasOwnProperty(c) && data[c].pk == liczba)
                                         cena_tyk.push(data[c].fields.cena_netto);
                                    }
                           });

                            for (var i = 0, l = dane.length; i < l; i++) {
                                $('#okiter').empty();
                                html.push(dane[i]);
                                $('#okiter').append(html);
                            }

                            for (var g = 0, d = cena.length; g < d; g++) {
                                $('#cenkii').empty();
                                html2.push(cena[g]);
                                $('#cenkii').append(html2);
                            }

                            for (var q = 0, f = cena_tyk.length; q < f; q++) {
                                count = parseFloat(cena_tyk[q]);
                                total += !isNaN(count) ? count : 0;
                            }

                        ofirt = parseFloat(cena_ofert);
                        var mokert = parseFloat(total);
                        var suma_ofert = ofirt + mokert;
                        var vat = parseFloat(23) / parseFloat(100);
                        var razem_vat = suma_ofert * vat;
                        var suma_ostat = suma_ofert + razem_vat;

                        var new_number = razem_vat.toFixed(2);
                        var suma_ostateczna = suma_ostat.toFixed(2);

                        $('#vat_suma').empty();
                        var ole = "name=\"vat_ter\"";
                        var ram = "name=\"razem_ter\"";
                        $('input[name=dodatki]').val(mokert.toFixed(2));
                        $('#vat_suma').append("<li "+ole+" value="+new_number+">"+new_number+" zł podatku</li>");

                        $('#razem_suma').empty();
                        $('input[name=amount]').val(parseFloat(suma_ofert).toFixed(2));
                        $('input[name=total_amount]').val(suma_ostateczna);
                        $('#razem_suma').append("<li "+ram+" value="+suma_ostateczna+">"+suma_ostateczna+" zł brutto</li>");

                    },
                    complete:function(){}
                });
            })
        })

        $('.daneimg').mouseover(function(e){
           $('.tooltip').css({'top':e.pageY,'left':e.pageX, 'z-index':'1'});
        });

});

