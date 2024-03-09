# Insights of this code challenge:
To get the extent of the fishnet map one has to know the minimum and maximum values of the coordinates in the CSV file.

For example, in this code the **Step_3_Cepphus_grylle.csv** file used the:
maximum longitude is -50.45<sup> 0</sup>, 
minimum longitude -82<sup> 0</sup>, 
maximum latitude is 59.43<sup> 0 </sup> and the
minimum latitide is 36.79312<sup> 0

These values gave me the extent of the fishnet map generation that will not consume time to generate bearing in mind the cell size width and height is 0.25.
