$(function(){

	var sentHead = "<div class='row' style='margin: 5px 0px'> <div class='col-sm-offset-4 col-sm-8 text-right'> <div class='sent text-left'>";
	var receivedHead = "<div class='row' style='margin: 5px 0px'> <div class='col-sm-8 text-left'> <div class='received text-left'>";
	var tail = "</div> </div> </div>";
	var sessionID = md5((Math.floor(Math.random() * 10000000000)).toString())
	
	console.log(sessionID)
	
	function send() {
		var data = {
			"message" : $("#message").val(),
			"sessionID" : sessionID
		};

		$('.chatdiv').append(sentHead+data.message+tail);
		$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);
		$("#message").val("");

		$.post("/",data,function(res){
			console.log(res)
			$('.chatdiv').append(receivedHead+res+tail);
			$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);

		});
		
		/*const client = new ApiAi.ApiAiClient({accessToken: '6d2145bdf1b4463c86d5c6bcc2f05b9c', sessionId : "session1"});
		let promise = client.textRequest(data.message);
		
		promise
		    .then(handleResponse)
    		.catch(heandleError);

		function handleResponse(serverResponse) {
		        console.log(serverResponse);
		        var res = serverResponse.result.fulfillment.speech;
		        $('.chatdiv').append(receivedHead+res+tail);
				$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);

		}
		function heandleError(serverError) {
		        console.log(serverError);
		}
*/

	};


	$("#message").keypress(function(event) {
		if (event.which == 13) {
			event.preventDefault();

			if( $("#message").val() != "")
				send();
		}
	});

	$("#rec").click(function(event) {
		switchRecognition();
		event.preventDefault();
		$("#rec").val("Listening...")
	});

	$("#send").click(function(event){
		send()
	})

	var recognition;

	function startRecognition() {
		recognition = new webkitSpeechRecognition();
		recognition.onstart = function(event) {
			updateRec();
		};
		recognition.onresult = function(event) {
			var text = "";
		    for (var i = event.resultIndex; i < event.results.length; ++i) {
		    	text += event.results[i][0].transcript;
		    }
		    console.log("text:");
		    console.log(text)

		    setInput(text);
			stopRecognition();
		};
		
		recognition.onend = function() {
			stopRecognition();
		};

		recognition.lang = "en-US";
		recognition.start();
	}

	function stopRecognition() {
		if (recognition) {
			recognition.stop();
			recognition = null;
		}
		updateRec();
	}

	function switchRecognition() {
		if (recognition) {
			stopRecognition();
		} else {
			startRecognition();
		}
	}

	function setInput(text) {
		$("#message").val(text);
		//send()
	}

	function updateRec() {
		//$("#rec").text(recognition ? "Stop" : "Speak");
		//$("#rec").html(recognition ? "<i class='fa fa-microphone-slash'></i>" : "<i class='fa fa-microphone'></i>")
		$("#rec").attr('class', recognition ? "fa fa-microphone micspan_on fa-lg" : "fa fa-microphone micspan fa-lg")

		//$("#message").val(recognition ? "Listening..." : "");
	}



});
