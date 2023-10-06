document.getElementById('feedback-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    let feedback = document.getElementById('feedback').value;
    let suggestions = document.getElementById('suggestions').value;
    let issues = document.getElementById('issues').value;
    
    // Incorporates Rule 6
    feedback = sensitiveLanguageFilter(feedback);
    suggestions = sensitiveLanguageFilter(suggestions);
    issues = sensitiveLanguageFilter(issues);
    
    // Save feedback, suggestions and issues into a database or send them to an API.
    saveFeedback(feedback, suggestions, issues);
    
    console.log("Feedback: " + feedback);
    console.log("Suggestions: " + suggestions);
    console.log("Issues: " + issues);

    alert("Your feedback has been successfully submitted. Thank you for your contribution!");
});

// Rule 6: Sensitive Language Filter
function sensitiveLanguageFilter(input) {
    const offensiveWords = ["badword1", "badword2"]; // replace with actual offensive words
    
    offensiveWords.forEach(word => {
        const regex = new RegExp(word, "gi");
        input = input.replace(regex, "***");
    });
    
    return input;
}

// Sample function that simulates saving data
function saveFeedback(feedback, suggestions, issues) {
    // Here, you should save the user's feedback to your database or send it to your API.
    // This is a placeholder function.
}