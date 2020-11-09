$(function() {
  setTimeout(function() {
    $(".alert").slideUp(3000);
  }, 5000);

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 
const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  beforeSend:(xhr) =>{
    xhr.setRequestHeader("X-CSRFTOKEN",  csrftoken)
  }
})

$(document).on('submit', '.post-comment-form', function (event) {
  event.preventDefault();
  const comment = document.getElementById('commentform');
  $.ajax({
    type:'POST',
    url:$(this).attr('action'), 
    data:{
      "comment": comment.value
    },
    dataType:'json',
    success:function(response){
      $("#main_comment_section").html(response['form']);
      $("input").val('');
      // comment.value = ""
    },
    error:function(rs,e){
      console.log(rs.responseText);
    }
  });
}); 


  // var usr = document.querySelector("#users").innerHTML;
  var subs = document.getElementById("sub").innerHTML;
  var vols = document.getElementById("voluns").innerHTML;
  var partners = document.getElementById("parts").innerHTML;
  var clients = document.getElementById("clients").innerHTML;
  // for the charts
  var ctx = document.getElementById("myChart");
  Chart.defaults.global.defaultFontFamily = "Lato";
  Chart.defaults.global.defaultFontSize = 15;
  Chart.defaults.global.defaultFontColor = "#fff";
  var myChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: [
        // "Employees",
        "Subscribers",
        "Volunteers",
        "Partners",
        // "Messaging",
        "Clients"
      ],
      datasets: [
        {
          label: "#",
          data: [ subs, vols, partners,clients],
          backgroundColor: [
            // "rgba(255,99,132,0.6)",
            "rgba(54,162,235,0.6)",
            "rgba(255,206,86,0.6)",
            "rgba(75,192,192,0.6)",
            // "rgba(153,102,255,0.6)",
            "rgba(153,302,455,0.8)",
          ],
          borderColor: "#777",
          borderWidth: 1,
          hoverBorderWidth: 3,
          hoverBorderColor: "#000"
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: "ORgeon of stars' Activities",
        fontSize: 20,
        fontColor: "#fff"
      },
      legend: {
        display: true,
        position: "right",
        labels: {
          fontColor: "#fff"
        }
      },
      tooltips: {
        // enable:false
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            }
          }
        ]
      }
    }
  });

//  students activity
  var students = document.getElementById("students").innerHTML;
  var gradeschool = document.getElementById("gradeschool").innerHTML;
  var preschool = document.getElementById("preschool").innerHTML;
  var kindergarten = document.getElementById("kindergarten").innerHTML;
  // for the charts
  var ctx = document.getElementById("myChart2");
  Chart.defaults.global.defaultFontFamily = "Lato";
  Chart.defaults.global.defaultFontSize = 15;
  Chart.defaults.global.defaultFontColor = "#fff";
  var myChart1 = new Chart(ctx, {
//    type: "doughnut",
    type: "pie",
    data: {
      labels: [
        "Total Students",
        "GradeSchool",
        "PreSchool",
        "Kindergarten",
        // "Messaging",
      ],
      datasets: [
        {
          label: "#",
          data: [students, gradeschool, preschool, kindergarten],
          backgroundColor: [
            "rgba(255,99,132,0.6)",
            "rgba(54,162,235,0.6)",
            "rgba(255,206,86,0.6)",
            "rgba(75,192,192,0.6)",

          ],
          borderColor: "#777",
          borderWidth: 1,
          hoverBorderWidth: 3,
          hoverBorderColor: "#000"
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: "Summer Tutoring Activities",
        fontSize: 20,
        fontColor: "#fff"
      },
      legend: {
        display: true,
        position: "right",
        labels: {
          fontColor: "#fff"
        }
      },
      tooltips: {
        // enable:false
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            }
          }
        ]
      }
    }
  });

  // summer school survey
  var useful = document.getElementById("useful").innerHTML;
  var participate = document.getElementById("participate").innerHTML;
  var recommend = document.getElementById("recommend").innerHTML;
  var something_new = document.getElementById("something_new").innerHTML;
  // for the charts
  var ctx = document.getElementById("myChart3");
  Chart.defaults.global.defaultFontFamily = "Lato";
  Chart.defaults.global.defaultFontSize = 15;
  Chart.defaults.global.defaultFontColor = "#fff";
  var myChart1 = new Chart(ctx, {
//    type: "doughnut",
    type: "doughnut",
    data: {
      labels: [
        "Summer School Useful",
        "Would Participate Again",
        "Would Recommend a Friend",
        "Kids learnt Something New",
        // "Messaging",
      ],
      datasets: [
        {
          label: "#",
          data: [useful, participate, recommend, something_new],
          backgroundColor: [
            "#3B8BEB",
            "#B23850",
            "#E7E3D4",
            "#8590AA",

          ],
          borderColor: "#777",
          borderWidth: 1,
          hoverBorderWidth: 3,
          hoverBorderColor: "#000"
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: "Summer School Survey Results",
        fontSize: 20,
        fontColor: "#fff"
      },
      legend: {
        display: true,
        position: "right",
        labels: {
          fontColor: "#fff"
        }
      },
      tooltips: {
        // enable:false
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            }
          }
        ]
      }
    }
  });
});
