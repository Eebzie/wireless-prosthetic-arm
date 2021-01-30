let today = new Date().getHours();
let timeOfDay = '';
if (today >= 6 && today < 12) {
   timeOfDay = 'Good morning';
    } else if (today >= 12 && today < 18) {
        timeOfDay = 'Good afternoon';
    } else if (today >= 18 && today < 24){
        timeOfDay = 'Good evening';
    } else {
        timeOfDay = 'Hello';
}
document.body.innerHTML = timeOfDay;


const profile = {
    name: {
        firstName: 'Gabrielle',
        lastName: 'Agustin',
    },
    sex: 'female',
    city: 'Toronto',

}
function greet(timeOfDay, firstName){
    return '${timeOfDay}, ${profile.name.firstName}';
}

// firstName,
// ${firstName!}

