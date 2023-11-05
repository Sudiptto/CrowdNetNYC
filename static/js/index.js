// NOTE THIS IS WHERE THE GOOGLE MAPS API + PARSED GEO DATA WILL TAKE PLACE IN 


setTimeout(function(){
    document.querySelector(".preloader").style.display = "none";
  }, 1000);
  
  if (!sessionStorage.getItem('page_reloaded')) {
    sessionStorage.setItem('page_reloaded', true);
    location.reload();
  }
  
  let map, infoWindow;
  // Create info
  
  
  function initMap() {
  
    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 40.650002, lng: -73.949997 },
      zoom: 15,
      disableDefaultUI: true,
      mapTypeId: 'satellite' 
      // fullscreenControl: false
    });
    infoWindow = new google.maps.InfoWindow();
    const locationButton = document.createElement("button");
    locationButton.textContent = "Current Location";
    locationButton.classList.add("center-button");
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(locationButton);
    /*
    Note this location kind of works but very glitchy
    let wifi_username = prompt("Please enter Wifi-Username: ");
    let wifi_password = prompt("Please enter Wifi-Password: ");
    console.log(wifi_username, wifi_password);
    alert("Do you understand that these have to be correct?")*/

    locationButton.addEventListener("click", () => {
      /* Note this location doesn't work 
    let wifi_username = prompt("Please enter Wifi-Username: ");
    let wifi_password = prompt("Please enter Wifi-Password: ");
    console.log(wifi_username, wifi_password);
    alert("Do you understand that these have to be correct?") */
      // Try HTML5 geolocation.
      if (navigator.geolocation) {
        
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };
            //console.log(position.coords.latitude);
  
            //infoWindow.setPosition(pos);
            //infoWindow.setContent("Location found.");
            infoWindow.open(map);
            map.setCenter(pos);
          },
          () => {
            handleLocationError(true, infoWindow, map.getCenter());
          }
        );
      } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
      }
     });
     
     google.maps.event.addListener(map, 'dblclick', function(event){
      let marker = new google.maps.Marker({
          position: event.latLng,
          map: map,
          draggable: true,
          icon: {
            url:"http://maps.google.com/mapfiles/ms/icons/pink-dot.png"
          }
       });
    
       google.maps.event.addListener(marker,'dblclick', function(event){
          marker.setMap(null);
          
       });
  
      let geocoder = new google.maps.Geocoder();
      let latLng = event.latLng;
      
      // Note this place works well, after the user clicks they will be met with a prompt
      let wifi_username = prompt("Please enter Wifi-Username: ");
      let wifi_password = prompt("Please enter Wifi-Password: ");

      let confirm_username = prompt("Please re-enter Username: ");
      let confirm_password = prompt("Please re-enter Password: ");

      // Verify if they match 

      if(wifi_username == confirm_username && confirm_password == confirm_password){
        alert("Matches! ")
      }
      else{
        alert("Does not match! ")
        location.reload();
      }
      //console.log(wifi_username, wifi_password);
    
      // Send a geocoding request to Google Maps Geocoding API.
      geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === google.maps.GeocoderStatus.OK) {
          // Extract the postal code (zipcode) from the geocoding results.
          const zipcode = findZipCodeInResults(results[0]);
  
          // Extract the exact latitude and longitude as strings.
          const latitude = latLng.lat().toString();
          const longitude = latLng.lng().toString();
      
          // Create an object with latitude, longitude, and zipcode.
          const locationData = {
            latitude: latitude,
            longitude: longitude,
            zipcode: zipcode,
            wifiPassword: wifi_password,
            wifiUsername: wifi_username,
          };

          console.log(locationData);
      
          // Send the location data to the server using a fetch request.
          fetch('/add_data', {
            method: 'POST',
            credentials: 'include',
            body: JSON.stringify(locationData),
            headers: { 'Content-Type': 'application/json' }
          }).then(() => location.reload());
        }
      });
      
      // Helper function to find the zipcode from geocoding results.
      function findZipCodeInResults(geocodeResult) {
        for (let component of geocodeResult.address_components) {
          if (component.types.includes('postal_code')) {
            return component.short_name;
          }
        }
        return null; // Return null if no zipcode is found.
      }})
     
  }
  
  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
      browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
  }
  
  window.initMap = initMap;

// DEVELOP A FUNCTION THAT RETURNS THE MAPS.GOOGLE.COM icons based on the SSID
function maps_icons(ssid){
  // NOTE ALL ICONS ARE FROM: Freepik
  let url_icon = ""
  if(ssid == 'LinkNYC Free Wi-Fi'){
    url_icon = 'static/icons/linkNYC.png'
  }
  else if(ssid == 'GuestWiFi'){
    url_icon = 'static/icons/guestwifi.png'
  }
  else if(ssid == 'TransitWirelessWiFi'){
    url_icon = 'static/icons/mta.png'
  }
  else if(ssid == 'NYPL' || ssid == 'BPLUNWIRED' || ssid == 'QBPL_WIRELESS'){
    url_icon = 'static/icons/library.png'
  }
  else{ // ALL OTHERS 
    url_icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
  }
  //console.log(url_icon);
  return url_icon;
  
}

// Fetch data from the Flask endpoint
fetch('/get_csv_data')
    .then(response => response.json())
    .then(data => {

        
        // Iterate over the data using a for loop
        const parsedData = JSON.parse(data);
        for (let i = 0; i < parsedData.length; i++) {
            const item = parsedData[i];
            let latitude = item['LAT'];
            let longitude = item['LON'];
            let ssid = item['SSID'];
            let internet_type = item['TYPE'];
            //console.log(latitude, longitude, ssid, internet_type);

        
            // DRAW MARKERS
            // MAKE A NEW MARKER CSV (CAN'T BE DELETED )
            let markerCSV = new google.maps.Marker({
              position: {lat: latitude, lng: longitude},
              icon: {
               url: maps_icons(ssid)
                //url: "./static/Button_Icon_Green.svg.png"
              },
              map: map,
              draggable: false
           });


           // ADD IN INFORMATION 
           var infowindow = new google.maps.InfoWindow({
            content: "<h1 style='color: black; font-size: 15, font: Times New Roman'>Free WiFi Spot</h1> </br> <p style='color: black; font-size: 15, font: Times New Roman'> Internet Type: " + internet_type + " </br> SSID: " + ssid+  " </br> Note that this is from our  <b style='color: black'>database!</b> </p>"
           });
           
           markerCSV.addListener('mouseover', function() {
            infowindow.open(map, markerCSV);
           });
    
           markerCSV.addListener('mouseout', function() {
            infowindow.close();
           });

        }
        // DEVELOP A FUNCTION THAT RETURNS THE MAPS.GOOGLE.COM icons based on the SSID

    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });


fetch('/data')
.then(response => response.json())
.then(data => {
    //console.log(data);
//    const geocoder = new google.maps.Geocoder();

// Code below starts at 0 and goes till end of the data.length (note that this depends on how large)

    for(let i = 0; i < data.length; i++){
      
        let markerA = new google.maps.Marker({
          position: {lat: data[i][0], lng: data[i][1]},
          icon: {
           url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            //url: "./static/Button_Icon_Green.svg.png"
          },
          map: map,
          draggable: false
       });
       
       
       
       let date = new Date(data[i][2]);
       //console.log(date)
       //console.log(data[i][3]); // this is the wifi username
       //console.log(data[i][4]); // this is the wifi password
       wifiUsername = data[i][3]
       wifiPassword = data[i][4]
       var infowindow = new google.maps.InfoWindow({
        content: "<h1 style='color: black; font-size: 20px'>User Added WiFi!</h1> <br/> <h3 style='color: black; font-size: 10px'>Wifi-Username: " +  wifiUsername +" </h3> <h3 style='color: black; font-size: 10px'>Wifi-Password: " +  wifiPassword +" </h3> <h3 style='color: black; font-size: 10px'>Date Posted: " +  date +" </h3> <p style='color: black; font-size: 15px'> Take with grain of salt, added by USER! </p>"
       });
       
       markerA.addListener('mouseover', function() {
        infowindow.open(map, markerA);
       });

       markerA.addListener('mouseout', function() {
        infowindow.close();
       });


       google.maps.event.addListener(markerA,'dblclick', function(event){
        markerA.setMap(null);
        let entry = JSON.stringify(event.latLng.toJSON(), null, 2)
        console.log(entry)
        
        fetch ('/delete_data', {
          method : "POST",
          credentials : 'include',
          body : JSON.stringify(entry),
          cache : "no-cache",
          headers : new Headers ({
            "content-type" :"application/json"
         })
       })
     });
       
      
    }
    
})   



  
 