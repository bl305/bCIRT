

/* Dropdown filter
When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function filterFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunction2() {
  document.getElementById("myDropdown2").classList.toggle("show");
}

function filterFunction2() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput2");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown2");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunctionInv() {
  document.getElementById("myDropdownInv").classList.toggle("show");
}

function filterFunctionInv() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputInv");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownInv");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunctionTask() {
  document.getElementById("myDropdownTask").classList.toggle("show");
}

function filterFunctionTask() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputTask");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownTask");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunctionTaskSelect() {
  document.getElementById("myDropdownTaskSelect").classList.toggle("show");
}

function filterFunctionTaskSelect() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputTaskSelect");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownTaskSelect");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunctionTaskTemplate() {
  document.getElementById("myDropdownTaskTemplate").classList.toggle("show");
}

function filterFunctionTaskTemplate() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputTaskTemplate");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownTaskTemplate");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunctionEv() {
  document.getElementById("myDropdownEv").classList.toggle("show");
}

function filterFunctionEv() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputEv");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownEv");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunctionEvFile() {
  document.getElementById("myDropdownEvFile").classList.toggle("show");
}

function filterFunctionEvFile() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputEvFile");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownEvFile");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterFunctionEvAttr() {
  document.getElementById("myDropdownEvAttr").classList.toggle("show");
}

function filterFunctionEvAttr() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputEvAttr");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownEvAttr");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}


function filterFunctionPlay() {
  document.getElementById("myDropdownPlay").classList.toggle("show");
}

function filterFunctionPlay() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInputPlay");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdownPlay");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}



//#NOT USED YET
function inv_del() {
  var isValid = confirm('Confirm DELETION:\nAre you sure you want to delete this Investigation?\n\nThis will delete all evidences documented under this investigation!!!');
  if (!isValid) {
     event.preventDefault();
     alert("INFO:\nCancelled!");
  }
  else {
    alert("INFO:\nYou selected to delete this Investigation!!!\n\nIt has not yet been deleted. You will have another chance to confirm deletion in the next popup.");
    var isValid2 = confirm('Repeat confirm of DELETION:\nAre you really sure you want to delete this Investigation??\n\nThis will delete ALL evidences documented under this investigation !!!');
    if (!isValid2) {
       event.preventDefault();
       alert("Cancelled!");
    }
    else {
        alert("Deleted, page will refresh!");
        location.reload();
    }
  }
}

function inv_assign() {
  var isValid = confirm('Confirm ASSIGNMENT\n\nAre you sure you want to assign this Investigation to you?');
  if (!isValid) {
     event.preventDefault();
     alert("INFO:\nCancelled!");
  }
  else {
        alert("Assigned, page will refresh!");
//        location.reload();
  }
}

function task_assign() {
  var isValid = confirm('Confirm ASSIGNMENT\n\nAre you sure you want to assign this Task to you?');
  if (!isValid) {
     event.preventDefault();
     alert("INFO:\nCancelled!");
  }
  else {
        alert("Assigned, page will refresh!");
//        location.reload();
  }
}

//dropdown
$(document).ready(function() {

    // For the Second level Dropdown menu, highlight the parent
    $( ".dropdown-menu" )
    .mouseenter(function() {
        $(this).parent('li').addClass('active');
    })
    .mouseleave(function() {
        $(this).parent('li').removeClass('active');
    });

});


// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
// When the user clicks on the bottom button, scroll to the bottom of the document
function bottomFunction() {
  window.scrollTo(0,document.body.scrollHeight);
//  document.body.scrollBottom = 0; // For Safari
//  document.documentElement.scrollBottom = 0; // For Chrome, Firefox, IE and Opera
}



///
$('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
  if (!$(this).next().hasClass('show')) {
    $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
  }
  var $subMenu = $(this).next(".dropdown-menu");
  $subMenu.toggleClass('show');


  $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
    $('.dropdown-submenu .show').removeClass("show");
  });


  return false;
});