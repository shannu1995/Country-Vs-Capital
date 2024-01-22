Note: The app performs personal requests without an access token. The limit for this per IP address is 500 per minute.
Please find more detail about such limits here: https://api.wikimedia.org/wiki/Rate_limits#:~:text=API%20requests%20authenticated%20using%20a,to%205%2C000%20requests%20per%20hour.

The program scrapes data from two Wikipedia links.

One is the list that contains the most popular country-related pages of Wikipedia.

The other is the list of national capitals.

Eventually the program will be a quiz that matches the country with it's capital.

The reason for downloading the popularity table is to use it to determine the dificulty of the quiz. If the user selects an "Easy" quiz, the program only shows the most popular countries.

If it is Medium, it should show countries in the middle of the popularity spectrum and if is Hard, the program will only show the most obscure countries.
