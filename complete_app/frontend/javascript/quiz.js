function shuffle(array) {
    let currentIndex = array.length,  randomIndex;
  
    // While there remain elements to shuffle.
    while (currentIndex != 0) {
  
      // Pick a remaining element.
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
  
      // And swap it with the current element.
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
  }
  
var question_array = ["What is the Dimension of the arena? (width:height)",
                      "What is the height:width of the tree?",
                      "What is the maximum number of fruits that can be put on one single line?",
                      "What is the Penalty for damaging the arena or displacing unripe fruits?",
                      "What is the maximum allowed time for each run(in minutes)?",
                      "how many points is given for each correctly deposited fruit?"];
                      // if you want to add more question, add it here

var options_array = [["<input type='radio' name='Q1' value='true'>130:140", "<input type='radio' name='Q1' value='false'>140:150", "<input type='radio' name='Q1' value='false'>140:130", "<input type='radio' name='Q1' value='false'>150:140"],
                    ["<input type='radio' name='Q2' value='true'>40:50", "<input type='radio' name='Q2' value='false'>35:40", "<input type='radio' name='Q2' value='false'>40:35", "<input type='radio' name='Q2' value='false'>40:45"],
                    ["<input type='radio' name='Q3' value='true'>3", "<input type='radio' name='Q3' value='false'>2", "<input type='radio' name='Q3' value='false'>4", "<input type='radio' name='Q3' value='false'>5"],
                    ["<input type='radio' name='Q4' value='true'>15", "<input type='radio' name='Q4' value='false'>10", "<input type='radio' name='Q4' value='false'>20", "<input type='radio' name='Q4' value='false'>5"],
                    ["<input type='radio' name='Q5' value='true'>10", "<input type='radio' name='Q5' value='false'>8", "<input type='radio' name='Q5' value='false'>5", "<input type='radio' name='Q5' value='false'>15"],
                    ["<input type='radio' name='Q6' value='true'>40", "<input type='radio' name='Q6' value='false'>50", "<input type='radio' name='Q6' value='false'>30", "<input type='radio' name='Q6' value='false'>25"]]
                    // for every question you must add its 4 options. each option format will be "<input type='radio' name='Q($question_no.)' value='($true if the option is true else false)'>($option)"

var answers_array = []

var index = [0, 1, 2, 3, 4, 5]; // the elements of this array should be all the numbers sequentially between 0-(question_array.length - 1)

ques_no = 1;
shuffle_index = shuffle(index);
shuffle_index.forEach(i => {
    item = document.getElementById("Q" + ques_no);
    shuffeled_options = shuffle(options_array[i]);
    let options = "<p>" + shuffeled_options[0] + "</p>" + "<p>" + shuffeled_options[1] + "</p>" + "<p>" + shuffeled_options[2] + "</p>" + "<p>" + shuffeled_options[3] + "</p>";
    item.innerHTML = "<h2>Q" + ques_no + " " + question_array[i] + "</h2>" + options;
    ques_no++;
});

function check()
{
  var c = 0;
  if(document.quiz.Q1.value == "true"){c++};
  if(document.quiz.Q2.value == "true"){c++};
  if(document.quiz.Q3.value == "true"){c++};
  if(document.quiz.Q4.value == "true"){c++};
  if(document.quiz.Q5.value == "true"){c++};
  if(document.quiz.Q6.value == "true"){c++};
  // if(document.quiz.Q7.value == "true"){c++};
  // if(document.quiz.Q8.value == "true"){c++};
  // if(document.quiz.Q9.value == "true"){c++}; and so on, as much question as you want
  confirm("you have scored " + (c*100/question_array.length).toString() + "%")
  location.replace('./screen_5_5.html')
  //document.write("you score " + c*100/question_array.length + "%");
}
