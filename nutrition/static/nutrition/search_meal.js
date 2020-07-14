document.addEventListener('DOMContentLoaded', function() {
  const meal_size = document.querySelector('#meal_size');
  const meal_type = document.querySelector('#meal_type');

  var options_full = ["Breakfast", "Lunch", "Dinner"];
  var options_snack = ["Snack"];
  var options_extra = ["Extra"];

  var options = options_full.map(option => `<option value =${option.toLowerCase()}>${option}</option>`).join('\n');
  meal_type.innerHTML = options;

  meal_size.addEventListener('change', () => {
    if (meal_size.value == "FULL SIZE"){
      options = options_full.map(option => `<option value =${option.toLowerCase()}>${option}</option>`).join('\n');
      meal_type.innerHTML = options;
    } else if ( meal_size.value == "SNACK SIZE" ) {
      options = options_snack.map(option => `<option value =${option.toLowerCase()}>${option}</option>`).join('\n');
      meal_type.innerHTML = options;
    } else {
      options = options_extra.map(option => `<option value =${option.toLowerCase()}>${option}</option>`).join('\n');
      meal_type.innerHTML = options;
    }


  });
});
