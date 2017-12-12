<!DOCTYPE html>

<html>

<head>
</head>

<body>
   <h1>Enter a link to shorten it:</h1>

   <form action='/shorten/' method='post'>
      {% csrf_token %}
      {{ link_form.as_p }}
      <input type='submit' value='Shorten' />
   </form>
</body>

</html>
