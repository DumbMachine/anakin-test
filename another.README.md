# Assignment 1.B: What ways can be used to scrape data from mobile apps?
1. Appium:
	Using the mobile brother/sister software to selenium to automate working of the app. Similar to what I did for grab with selenium.
2. **Aunty Method**, eavesdropping _network_ calls:
	Proxy requests using charles or mitmproxy while performing manual actions on the app to index request/respones for reverse engineering.
	Problems with this method:
	- Semi scalable: The secrets used in the requests could be generated on the fly on the basis of fingerprinting information like current time. So this method is as scalable as those secrets are, if the secrets used by the app don't expire then one won't have problems here ( besides rate-limiting if one goes bonkers ).
	- Authentication: User authentication information was generated when the app was login ( manually ), creating a dependency to manually login to refresh authentication information ( in the case access_tokens expire )
	- Certificate Pinning: Intercepting requests would not work if the apps is strict. 
	This method works best in the environment where have a requirement to create a solid scraper which doesn't miss. Combination of manually logging in ( or automating this via scripts ) to devices to generate auth information and then using scripts to direct fetch data from APIs discovered by the proxy.
3. **Going in deep**:
	Going all the way with reverse engineering whatever stops one from making request from **not the app**.
	1. Pinning: Using a rooted android phone and injecting [this](https://github.com/Fuzion24/JustTrustMe) to disable ssl pinning.
		With this done, we can atleast intercept network calls via proxy.
	2. Fingerprint: It is possible to read traces and find stack calls where fingerprinting happens to grab private key and variables used. [HopperApp](https://www.hopperapp.com/) on jailbroken iphones seems to do it. I have never decompiled a program to reverse engineer it, so I would refrain from talking more about it here ( since all I would be doing now would be quoting lines from either blogs like [this](https://blog.tendigi.com/starbucks-should-really-make-their-apis-public-6b64a1c2e923)  or [this](https://www.toptal.com/back-end/reverse-engineering-the-private-api-hacking-your-couch) or the apps' own page )
	I guess I would say this is the Aunty Method, but the Aunty is a hacker and knows how to reverse engineering security checks.
	

# Assignment 2: App scraping
Find a scalable way to fetch all restro and menu information from Careem App.

## Methodology:
Aim:
Getting the API calls to fetch **restaurants** information in an area, since we can generate area information ourselves ( coordinates of locations ). Now that we will have list of restaurants in a location, we use the `restaurant.id` attribute to find menu information from the second API.

Mitmproxy:
Used a proxy to read all network calls made by ios *careem* app. Refreshing restro listing pages to capture and filter api call for getting the responsible api.  Did the same for getting menu information.


Some variables:
```
// <loc_name> : [lat ,lng]
locations: {
	"Burj Khalifa": [25.19698825061838, 55.27421546338867],
	"Al Deira": [25.270525,55.330440521240234]
}
// name of restraunts to fetch menu from
restaurants: [
	"Mannoushe Street",
	"Shake Shack",
]Ï
```


Deliverables:
1. Http requests to get information from the app
	1. GET restro information
	2. GET menu information for restro
2. Example showcasing the usage for the above with many variables

## Request Showcase:
<sub><sup>Responses have been cross-checked with data from the app</sup></sub>


<details>
	<summary>Fetching results for Restro near <b>Burj Khalifa 🏛</b></summary>
Request:
	<br>
<code>
 curl --header "Accept: application/json" --compressed --header "Accept-Language: en;q=1.0,en;q=0.9" --header "Agent: ICMA" --header "Application: careemfood-mobile-v1" --header "Authorization: Bearer eyJraWQiOiIwMTkyZTM5ZC1kZTgwLTQyZTEtYTdiYS00MDBkYzgwMTk5ODQiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1MzE5NDYzNCIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NTMxOTQ2MzQsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJzY29wZSI6InN1YnNjcmlwdGlvbnMgYWRkcmVzcyB3YWxsZXQgb3BlbmlkIHhjbWEgcHJvZmlsZSBwYXltZW50cyBhdXRoX3YxX3Rva2VuIGRlbGl2ZXJpZXMgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTYzNTY1NDEwNCwiaWF0IjoxNjM1NTY3NzA0LCJqdGkiOiJiNTA4MDQ5MS0zNmMwLTQyNGItOGU5MC1lYjY3ZTgxMWVlMjMifQ.LMgdDO3mvAWSCuqqJLE6JLnIv7QtXkqEkfnSFI0zYv8OD3wDlLypCZPhA321zB03PkLbYew1kKZZXZq5fo0qRYuZNQfo6Ooac_h5LhGM2LT8PH9vGGPk7Iyv45zXYb9b2xSCdUF9C3G1om71jL6bUjvAYE1INqvnsofG0UcapBi3cJbZUyMDWRRxk459cXEBeF7aZkvYcsZMFe9j_aIuLL_zjCid68OV8TSfPyE-lVRLZx9FIeIgOACXqdXI4qF2pYalt2zokqWKOKaGcALxHptozys6qoqxgO2kFr9Qv4ixNDNG8K0BvotA3oF5uIk-Hc3kB9kw7tmh2ezEWdnMig" --header "City-Id: 1" --header "Device: FF46DFC1-6498-40AE-8663-AB810CC52910" --header "Lat: 25.275897979736328" --header "Lng: 55.330440521240234" --header "Meta: ios;production;14.31.0 (1);15.1;iPhone14,2" --header "Time-Zone: Asia/Dubai" --user-agent "ICMA/11.42.1" --header "Uuid: 08D6B5B6-DE91-40EB-8164-EF905428F061" --header "Version: 11.42.1" --header "X-Careem-Agent: ICMA" --header "X-Careem-Beta: false" --header "X-Careem-Version: 11.42.1" --header "X-Careemdomain: food" --header "X-request-Source: SUPERAPP" "https://apigateway.careemdash.com//v2/discover?reorder_variant=recommended&include_offers=1" 
<code/>
	
Response:
<br>
<p>
<a href="https://github.com/DumbMachine/anakin-test/blob/master/get.1.bj.json">Click here to see response</a>
	</p>

</details>
	
	

<details>
	<summary>Fetching results for Restro near <b>Al Deira 🎆 </b></summary>
Request:
	<br>
<code>
 curl --header "Accept: application/json" --compressed --header "Accept-Language: en;q=1.0,en;q=0.9" --header "Agent: ICMA" --header "Application: careemfood-mobile-v1" --header "Authorization: Bearer eyJraWQiOiIwMTkyZTM5ZC1kZTgwLTQyZTEtYTdiYS00MDBkYzgwMTk5ODQiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1MzE5NDYzNCIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NTMxOTQ2MzQsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJzY29wZSI6InN1YnNjcmlwdGlvbnMgYWRkcmVzcyB3YWxsZXQgb3BlbmlkIHhjbWEgcHJvZmlsZSBwYXltZW50cyBhdXRoX3YxX3Rva2VuIGRlbGl2ZXJpZXMgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTYzNTY1NDEwNCwiaWF0IjoxNjM1NTY3NzA0LCJqdGkiOiJiNTA4MDQ5MS0zNmMwLTQyNGItOGU5MC1lYjY3ZTgxMWVlMjMifQ.LMgdDO3mvAWSCuqqJLE6JLnIv7QtXkqEkfnSFI0zYv8OD3wDlLypCZPhA321zB03PkLbYew1kKZZXZq5fo0qRYuZNQfo6Ooac_h5LhGM2LT8PH9vGGPk7Iyv45zXYb9b2xSCdUF9C3G1om71jL6bUjvAYE1INqvnsofG0UcapBi3cJbZUyMDWRRxk459cXEBeF7aZkvYcsZMFe9j_aIuLL_zjCid68OV8TSfPyE-lVRLZx9FIeIgOACXqdXI4qF2pYalt2zokqWKOKaGcALxHptozys6qoqxgO2kFr9Qv4ixNDNG8K0BvotA3oF5uIk-Hc3kB9kw7tmh2ezEWdnMig" --header "City-Id: 1" --header "Device: FF46DFC1-6498-40AE-8663-AB810CC52910" --header "Lat: 25.270525" --header "Lng: 55.330440521240234" --header "Meta: ios;production;14.31.0 (1);15.1;iPhone14,2" --header "Time-Zone: Asia/Dubai" --user-agent "ICMA/11.42.1" --header "Uuid: 08D6B5B6-DE91-40EB-8164-EF905428F061" --header "Version: 11.42.1" --header "X-Careem-Agent: ICMA" --header "X-Careem-Beta: false" --header "X-Careem-Version: 11.42.1" --header "X-Careemdomain: food" --header "X-request-Source: SUPERAPP" "https://apigateway.careemdash.com//v2/discover?reorder_variant=recommended&include_offers=1" 
<code/>
	
Response:
<br>
<p>
<a href="https://github.com/DumbMachine/anakin-test/blob/master/get.ald.json">Click here to see response</a>
	</p>

</details>
	
	
<details>
	<summary>Fetching results for Menu Item for <b>Man'oushe Street 👳</b></summary>
Image:
	<br>
	<img src="https://user-images.githubusercontent.com/23381512/139527853-08f2632a-0309-46dd-a641-7f154d8c3bd8.png">
	<br>
	Request:
	<br>
<code>
curl --header "accept: application/json" --compressed --header "accept-language: en;q=1.0,en;q=0.9" --header "agent: ICMA" --header "application: careemfood-mobile-v1" --header "authorization: Bearer eyJraWQiOiIwMTkyZTM5ZC1kZTgwLTQyZTEtYTdiYS00MDBkYzgwMTk5ODQiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1MzE5NDYzNCIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NTMxOTQ2MzQsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJzY29wZSI6InN1YnNjcmlwdGlvbnMgYWRkcmVzcyB3YWxsZXQgb3BlbmlkIHhjbWEgcHJvZmlsZSBwYXltZW50cyBhdXRoX3YxX3Rva2VuIGRlbGl2ZXJpZXMgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTYzNTY1NDEwNCwiaWF0IjoxNjM1NTY3NzA0LCJqdGkiOiJiNTA4MDQ5MS0zNmMwLTQyNGItOGU5MC1lYjY3ZTgxMWVlMjMifQ.LMgdDO3mvAWSCuqqJLE6JLnIv7QtXkqEkfnSFI0zYv8OD3wDlLypCZPhA321zB03PkLbYew1kKZZXZq5fo0qRYuZNQfo6Ooac_h5LhGM2LT8PH9vGGPk7Iyv45zXYb9b2xSCdUF9C3G1om71jL6bUjvAYE1INqvnsofG0UcapBi3cJbZUyMDWRRxk459cXEBeF7aZkvYcsZMFe9j_aIuLL_zjCid68OV8TSfPyE-lVRLZx9FIeIgOACXqdXI4qF2pYalt2zokqWKOKaGcALxHptozys6qoqxgO2kFr9Qv4ixNDNG8K0BvotA3oF5uIk-Hc3kB9kw7tmh2ezEWdnMig" --header "city-id: 1" --header "device: FF46DFC1-6498-40AE-8663-AB810CC52910" --header "lat: 25.196929931640625" --header "lng: 55.274391174316406" --header "meta: ios;production;14.31.0 (1);15.1;iPhone14,2" --header "time-zone: Asia/Dubai" --user-agent "ICMA/11.42.1" --header "uuid: 08D6B5B6-DE91-40EB-8164-EF905428F061" --header "version: 11.42.1" --header "x-careem-agent: ICMA" --header "x-careem-beta: false" --header "x-careem-version: 11.42.1" --header "x-careemdomain: food" --header "x-request-source: SUPERAPP" "https://apigateway.careemdash.com//v1/restaurants/897330?offers_category=0" 
<code/>
	
Response:
<br>
<p>
<a href="https://github.com/DumbMachine/anakin-test/blob/master/menu.1.json">Click here to see response</a>
	</p>

</details>
	
	
	
		
<details>
	<summary>Fetching results for Menu Item for <b>Shake Shack🍔</b></summary>
Image:
	<br>
	<img src="https://user-images.githubusercontent.com/23381512/139527848-1d41bd48-cf18-4b0f-b4de-f7cd0af78f01.png">
	<br>
	Request:
	<br>
<code>
curl --header "accept: application/json" --compressed --header "accept-language: en;q=1.0,en;q=0.9" --header "agent: ICMA" --header "application: careemfood-mobile-v1" --header "authorization: Bearer eyJraWQiOiIwMTkyZTM5ZC1kZTgwLTQyZTEtYTdiYS00MDBkYzgwMTk5ODQiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1MzE5NDYzNCIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NTMxOTQ2MzQsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJzY29wZSI6InN1YnNjcmlwdGlvbnMgYWRkcmVzcyB3YWxsZXQgb3BlbmlkIHhjbWEgcHJvZmlsZSBwYXltZW50cyBhdXRoX3YxX3Rva2VuIGRlbGl2ZXJpZXMgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTYzNTY1NDEwNCwiaWF0IjoxNjM1NTY3NzA0LCJqdGkiOiJiNTA4MDQ5MS0zNmMwLTQyNGItOGU5MC1lYjY3ZTgxMWVlMjMifQ.LMgdDO3mvAWSCuqqJLE6JLnIv7QtXkqEkfnSFI0zYv8OD3wDlLypCZPhA321zB03PkLbYew1kKZZXZq5fo0qRYuZNQfo6Ooac_h5LhGM2LT8PH9vGGPk7Iyv45zXYb9b2xSCdUF9C3G1om71jL6bUjvAYE1INqvnsofG0UcapBi3cJbZUyMDWRRxk459cXEBeF7aZkvYcsZMFe9j_aIuLL_zjCid68OV8TSfPyE-lVRLZx9FIeIgOACXqdXI4qF2pYalt2zokqWKOKaGcALxHptozys6qoqxgO2kFr9Qv4ixNDNG8K0BvotA3oF5uIk-Hc3kB9kw7tmh2ezEWdnMig" --header "city-id: 1" --header "device: FF46DFC1-6498-40AE-8663-AB810CC52910" --header "lat: 25.196929931640625" --header "lng: 55.274391174316406" --header "meta: ios;production;14.31.0 (1);15.1;iPhone14,2" --header "time-zone: Asia/Dubai" --user-agent "ICMA/11.42.1" --header "uuid: 08D6B5B6-DE91-40EB-8164-EF905428F061" --header "version: 11.42.1" --header "x-careem-agent: ICMA" --header "x-careem-beta: false" --header "x-careem-version: 11.42.1" --header "x-careemdomain: food" --header "x-request-source: SUPERAPP" "https://apigateway.careemdash.com//v1/restaurants/2828?offers_category=0" 
<code/>
	
Response:
<br>
<p>
<a href="https://github.com/DumbMachine/anakin-test/blob/master/menu.2.json">Click here to see response</a>
	</p>

</details>
	
