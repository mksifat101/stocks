
const csrftoken = getCookie("csrftoken");

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(";");
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == " ") {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

const postJson = (url, data, redirectTo) => {
  fetch(url, {
    method: 'POST',
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      "Accept-Encoding": "gzip,deflate,br",
      "X-CSRFToken": csrftoken,
    },
    body: data,
  })
  .then((response) => {
    //window.open(redirectTo, "_self");
    console.log(response)
    return response.json()
  })
  .then((data) => {
    console.log(data)
  })
}

const updateJson = (url, data,redirectTo)  => {
  fetch(url, {
    method: 'PUT',
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      "Accept-Encoding": "gzip,deflate,br",
      "X-CSRFToken": csrftoken,      
    },
    body: data,
   
  })
  .then((response) => {
    //window.open(redirectTo, "_self");
    if(!response.ok){
      DisplayMessage('','Some Error Occured',false)
    }
    else{
      window.open(redirectTo, "_self");
    }
    
  })
  .then((data) => {
    console.log(data)
    window.open(redirectTo, "_self");
    //DisplayMessage('','Category Deleted Successfully')
  })
}

const DeleteEntity = (url, redirectTo) => {
  debugger
  fetch(url, {
    method: 'DELETE',
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      "Accept-Encoding": "gzip,deflate,br",
      "X-CSRFToken": csrftoken,
    },
   
  })
  .then((response) => {
    //window.open(redirectTo, "_self");
    if(!response.ok){
      DisplayMessage('','Some Error Occured',false)
    }
    else{
      //window.open(redirectTo, "_self");
      return response.json()
    }
    
  })
  .then((data) => {
    console.log(data)
    //DisplayMessage('',data['detail'],data['status'])
    window.open(redirectTo, "_self");
    //DisplayMessage('','Category Deleted Successfully')
  })
}

// const SaveWarehouse = () => {
//   let formdata = new FormData();
//     debugger
//     data = JSON.stringify({
//         'name': 'SampleWarehouse',
//         'code': 'Warehouse39',
//     })
//     fetch('/api/warehouse/create',{
//     method: "POST",
//     headers: {
//         Accept: "application/json, text/plain, */*",
//         "Content-Type": "application/json",
//         "Accept-Encoding": "gzip,deflate,br",
//         "X-CSRFToken": csrftoken,
//       },
//     body: data,
//     }).then((response) => {
//         console.log(response)
//     }).then((data) => {
//         console.log(response)
//     })

// }

// function itemFunc (e) {
//   let item_div = document.createElement('div');
//   let input = e.target.value
  
//   console.log(input)
//   fetch("../api/items/search/?item="+input,{            
//   method: "GET",
//   headers: {
//   Accept: "application/json, text/plain, */*",
//   "Content-Type": "application/json",
//   "Accept-Encoding": "gzip,deflate,br",
//   "X-CSRFToken": csrftoken,
// },
//   })
//   .then((response) => {
//       debugger
//       console.log(response)
//       if (!response.ok) {
//           console.log(response);
//           response.text().then((text) => {
//           let detail = JSON.parse(text).detail[0];
//           //DisplayMessage("", detail, false);
//           });
// } else {
//   return response.json();
// }
//   }).then((data) => {
//       debugger            
//       let menu = document.getElementById('itemMenu')
//       let item = ''
//       let itemData = ''
//       for(let i=0; i < data.length; i++){
          
//           itemData =JSON.stringify(data[i])
//           if(data[i]['track_variant'] == true){
//               let variantNames = []
//               let optionNames = []
//               for(let k=0; k < data[i]['variant'].length; k++){
//                   variantNames.push(data[i]['variant'][k]['name'].toString())
//                   for(let j=0; j < data[i]['variant'][k]['option'].length; j++){
//                       optionNames.push(data[i]['variant'][k]['option'][j]['name'].toString())
//                   }
//               }                    
              
//               arrayVariants = setVariants(data[i]['variant'])
//               //memory = `<input type="hidden" value= />`
//               item += `<div class="item" onclick='AddItemVariant(${itemData})'> 
//                       <span>${data[i]['name']}</span>
//                   </div>`
//           }
//           else{
//               item += `<div class="item" onclick='setItemTable(${itemData})'> ${data[i]['name']}</div>`
//           }                
//       }
//       menu.innerHTML = item
//       //menu.appendChild(item_div)
//   })
// }

function checkItemOptions(data){
  debugger       
  
  let result = []
  let selectedVariants = []
  let selectedOptions = []
  //let variantsCount = elem.parentElement.parentElement.childElementCount;
  let variantDiv = document.getElementById('item_variant')   
  let count = variantDiv.childElementCount     
  for(let i=0; i < variantDiv.childElementCount ; i++){
      let dict = {}
      if (variantDiv.children[i].querySelector('select').value != 0){                
          count--               
      }
      selectedVariants[i] = variantDiv.children[i].querySelector('label').innerText
      dict['name'] = variantDiv.children[i].querySelector('label').innerText 
      selectedOptions[i] = variantDiv.children[i].querySelector('select').value
      dict['option'] = variantDiv.children[i].querySelector('select').value 
      result.push(dict)
      if(count == 0){
          //dict['name'] = selectedVariants
          //dict['option'] = selectedOptions
          
          setItemTable(data, result)
          $('.ui.modal').modal('hide');
      }
  }
}

function setItemTable(data, variants){
  let units = document.getElementById('units_hf').value
  let itemTable = document.getElementById("itemsTable")
  units = units.split(',')
  let unitCell = '<select class="ui selection dropdown">'
  let a = []
  for (let j = 0; j < units.length; j++) {
      a = units[j].split(':')
          unitCell += `<option value='${a[1]}'> ${a[0]} </option>`
      }
  unitCell += '</select>'

  // let row = `
  //         <tr>
  //             <td> ${data['name']} (${data['code']}) </td>
  //             <td> <input type="text" /> </td>
  //             <td> <input type="text" /> </td>
  //             <td>
  //                 ${unitCell}
  //             </td>
  //             </tr>
  //         `
  let newRow = itemTable.insertRow();
  let newCell1 = newRow.insertCell();
  let content = `${data['name']} (${data['code']})
  <br/>`
  if(variants != undefined){
    content +=  `<div id="selected-variant">`
  for(let i = 0; i < variants.length; i++){
      content +=`
      <div>
      <label class="boldSpan" value='${variants[i]['id']}'>${variants[i]['name']} </label> : <label value='${variants[i]['option']}'>${variants[i]['option']}</label><br/>
      </div>
      
      `
  }
  
}

let variantsItem = document.getElementsByName('selectedVariantValue')
let optionsItem = document.getElementsByName('selectedOptionValue')


for(let h=0; h < optionsItem.length; h++){
  content += `<input value='${optionsItem[h].value}' name="selectedOptionValueTable" type="hidden">  `
}

for(let k=0; k < variantsItem.length; k++){
  content += `<input value='${variantsItem[k].value}' name="selectedVariantValueTable" type="hidden"> `
}
content += '</div>'
  newCell1.innerHTML = content
  
  newCell1.value = `${data['id']}`
  let track_weight = data['track_weight']
  let newCell2 = newRow.insertCell()
  if(track_weight)
  content = `<input type="number" placeholder="Enter Weight in kg" value=1/>`
  else
  content = `<span>Track Weight <i class="red close icon"></i>  </span>`
  newCell2.innerHTML = content
  let newCell3 = newRow.insertCell()
  content = `<input type="number" value=1 />`
  newCell3.innerHTML = content
  let newCell4 = newRow.insertCell()
  content = `${unitCell}`
  newCell4.innerHTML = content
}

function AddItemVariant(data){
  debugger
  let variantDiv = ''
  let optionDropdown = ''
  let variantName = ''
  let variants = data['variant']
  for(let i=0; i < variants.length; i++){
      variantName = variants[i]['name']
      variantDiv += `<div class="field"> 
      <input type="hidden" class='${variants[i]['name']}' name="selectedVariantValue" value='${variants[i]['id']}'>
      <label value='${variants[i]['id']}'> ${variantName} </label>`

      optionDropdown = `
      <select class="ui fluid selection dropdown ${variants[i]['name']}" name="selectedOptionValue"
      onchange='checkItemOptions(${JSON.stringify(data)})'><option value="" disabled selected> 
      ${variantName} </option>`
             
      for(let j=0; j < variants[i]['option'].length; j++){               
      optionDropdown += `
      <option value="${variants[i]["option"][j]["id"]}">
      ${variants[i]["option"][j]["name"]} </option>               
          `
      }
      optionDropdown += '</select>'
      variantDiv += optionDropdown
      variantDiv += '</div>'
  }
  
  // for(let k = 0; k < arr1.length; k++){
  //     console.log(arr1[k])
  //     variantDiv += '<div class="field">  <label>'
  //     variantDiv += `${arr1[k]}`
  //     variantDiv += '</label>'
  //     for(let k = 0;k < arr2.length; k++){
  //         console.log(arr2[k])
  //         optionDropdown += '<select class="ui dropdown">'
  //         optionDropdown += `
  //                 <option value=${arr2[k]}>${arr2[k]}</option>               
  //         `
  //     }
  //     optionDropdown += '</select>'
  //     variantDiv += optionDropdown
  // variantDiv += '</div>'
  // }                     
      document.getElementById('item_variant').innerHTML = variantDiv
      $('.ui.modal')
      .modal('show');
}



const postFormData = (url, formData, redirectTo) => {
  var headers = new Headers();
  // headers.append("Cookie", `csrftoken =${csrftoken}`);
  
  headers.append("X-CSRFToken", `${csrftoken}`);
  headers.append("X-Requested-With", "XMLHttpRequest");
  let requestOptions = "";

//   if (url == "api/product/add/") {
    requestOptions = {
      method: "POST",
      headers: headers,
      body: formData,
      redirect: "follow",
      credentials: 'include',
    };
    fetch(url, requestOptions)
    .then((response) => {
      //response.text()
      if (!response.ok) {
        console.log(response);
        // response.text().then((text) => {
        //   DisplayMessage(
        //     "",
        //     "Some Error Occurred. Please try again after some time.",
        //     false
        //   );
        //   return false;
        // });
        // response.text().then((text) => {
        //   let detail = JSON.parse(text).detail;
        //   DisplayMessage("", detail, false);
        // });
        response.text().then((text) => {
          DisplayMessage(
            "",
            "Some Error Occurred. Please try again after some time.",
            false
          );
        });
        
      }
      else{
        return response.json();
      }
    })
    .then((data) => {
      ShowResult(data, redirectTo);
      window.open(redirectTo, "_self");
    })
    .catch((error) => {
      console.log("error", error)
    });

}

const editFormData = (url, formData, redirectTo) => {
  var headers = new Headers();
  headers.append("Cookie", `csrftoken =${csrftoken}`);
  headers.append("X-Requested-With", "XMLHttpRequest");
  headers.append("X-CSRFToken", `${csrftoken}`);
  let requestOptions = "";

//   if (url == "api/product/add/") {
    requestOptions = {
      method: "PUT",
      headers: headers,
      body: formData,
      redirect: "follow",
    };
    fetch(url, requestOptions)
    .then((response) => {
      //response.text()
      if (!response.ok) {
        console.log(response);
        response.text().then((text) => {
          DisplayMessage(
            "",
            "Some Error Occurred. Please try again after some time.",
            false
          );
        });
      }
      else{
        return response.json();
      }
    })
    .then((data) => {
      //ShowResult(data, redirectTo);
      window.open(redirectTo, "_self");
    })
    .catch((error) => console.log("error", error));

}


const ShowResult = (data, redirectTo) => {
  var detail = data.detail;
  var status = data.status;
  if (status == false) {
    switch (data.detail) {
      case "Either phone or otp was not received":
        DisplayMessage("Required Data missing", data.detail, data.status);
        break;

      default:
        DisplayMessage(
          "Some Error Occured.Please try again later",
          data.detail,
          data.status
        );
        break;
    }
  } else {
    switch (data.detail) {
      case "An SMS with an OTP(One Time Password) has been sent <br/> to your Mobile number":
        OpenMobileVerification();
        DisplayMessage("", data.detail, data.status);
        document.querySelector("#mobileField").classList.add("hidden");
        break;
      case "User registered successfully":
        debugger;
        var pft = document.getElementById("password").value;
        var mobile_no = document.getElementById("mobile_no").value;
        debugger;
        document.getElementById("otpVerificationDiv").style.display = "none";
        $(".ui.modal").modal("show");

        let jsonBody = JSON.stringify({
          phone: mobile_no,
          pft: pft,
        });
        postJSON("/api/login/", jsonBody);
        debugger;
        setTimeout(() => {
          window.open("/", "_self");
        }, 2000);
        break;

      
      case "OTP matched.Now you can create new password":
        DisplayMessage("OTP matched", "Enter your new password", true);
        document.getElementById("otpVerificationDiv").style.display = "none";
        document.getElementById("change_password_div").style.display = "block";

        break;
      case "Logged in Successfully":
        ProceedLogin(data);

        break;

      
      case "Image uploaded succcesfully":
        DisplayMessage(
          "",
          "Store Successfully Created. Now you are ready to list your products online and reach your customers.",
          true
        );
      case "You have been logged out Successfully.":
        if (redirectTo != undefined && redirectTo != null && redirectTo != "") {
          DisplayMessage(
            "Logged out successfully",
            "Switch to a different account",
            data.status
          );
          setTimeout(() => {
            window.open(redirectTo, "_self");
          }, 2000);
          break;
        }
        DisplayMessage("", data.detail, data.status);
        setTimeout(() => {
          window.open("/", "_self");
        }, 2000);
        break;
      
     
     
      
      
      case "Password changed successfully.Login to your account":
        window.location.href = "/login";
        break;
      default:      
        window.open(redirectTo, "_self");  
        DisplayMessage("", data.detail, data.status);
    }
  }
};


const DisplayMessage = (heading, detail, status) => {
  debugger;
  switch (status.toString()) {
    case "true":
      document.querySelector(".showMessage").classList.remove("error");
      document.querySelector(".showMessage").classList.add("success");
      break;
    case "false":
      document.querySelector(".showMessage").classList.remove("success");
      document.querySelector(".showMessage").classList.add("error");
      $('.ui.modal').modal('hide');
      break;
    case "info":
      document.querySelector(".showMessage").classList.remove("success");
      document.querySelector(".showMessage").classList.remove("error");
      document.querySelector(".showMessage").classList.add("info");
      break;
  }

  document.querySelector(".showMessage").style.display = "block";
  document.querySelector(".showMessage>div").innerText = heading;
  document.querySelector(".showMessage>p").innerHTML =
    typeof detail == "object" ? (detail.length == 0 ? "" : detail[0]) : detail;
  // if (heading == "") OpenMessageBar(detail);
  // else OpenMessageBar(heading);

  window.scrollBy(0, 0);
  $(".message").transition("bounce");
};

$( document ).ready(function() {
  $('#itemdropdown').dropdown();
});

function GoToPage(url){
  window.open(url, "_self");
}

const plusminusVariant = (elem, operation) => {
  let num = document.getElementById(elem).value
  debugger 
  switch (operation) {
      case '+':
          if (elem.toString().includes("pockets") && parseInt(num) >= 99)
              break;
          num = parseInt(num) + 1
          document.getElementById(elem).value = num
          break;

      case '-':
          if (parseInt(num) <= 0)
              break;
          num = parseInt(num) - 1
          document.getElementById(elem).value = num
          break;
  }
}

const plusminusOption = (elem, operation) => {
  let num = document.getElementById(elem).value
  debugger
  switch (operation) {
      case '+':
          if (elem.toString().includes("pockets") && parseInt(num) >= 99)
              break;
          num = parseInt(num) + 1
          document.getElementById(elem).value = num
          break;

      case '-':
          if (parseInt(num) <= 0)
              break;
          num = parseInt(num) - 1
          document.getElementById(elem).value = num
          break;
  }
}

function OpenDeleteModal(url, redirectTo){
  debugger
  $('#delete-modal').modal('show');
  $('.ui.modal').modal('show');

  document.getElementById('delete-button').addEventListener("click", function(){
    DeleteEntity(url,redirectTo)
  })

  document.getElementById('cancel-button').addEventListener("click", function(){
    $('.ui.modal').modal('hide');
  })
}