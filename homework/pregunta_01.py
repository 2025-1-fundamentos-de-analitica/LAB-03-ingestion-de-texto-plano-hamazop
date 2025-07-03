"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
import pandas

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    archivo = open("files/input/clusters_report.txt", "r").readlines()

    # Process the header

    # Extract it
    parte1 = list( filter( None, re.split("\s{2,}", archivo[0]) ) )
    parte2 = list( filter( None, re.split("\s{2,}", archivo[1]) ) )

    parte1 = [s.replace("\n", "") for s in parte1]
    parte2 = [s.replace("\n", "") for s in parte2]

    # Build it
    cabecera = parte1[0]

    for i in range( len( parte2 ) ):
      cabecera = cabecera + "\t" + parte1[i + 1] + " " + parte2[i]

    cabecera = cabecera + "\t" + parte1[-1]

    # Format it
    cabecera = cabecera.lower().replace(" ", "_").split("\t")

    # Create the Data Frame
    data_frame = pandas.DataFrame(columns = cabecera)

    # Remove header from original variable
    cuerpo = []
    EsCuerpo = False

    for linea in archivo:

      # Check for underscore
      match = re.search("-", linea)

      # If found
      if match and not EsCuerpo:

        # It means we are already in the body, so flag it
        EsCuerpo = True
      
      # If not found it means it is not a division line
      else:

        # Check if we are on the body

        # If we are, keep the line
        if EsCuerpo:
          cuerpo.append(linea)

        # If we are not, just skip the line
        else:
          pass
    # Process the body

    new_line = ""
    cluster = 0
    cantidad = 0
    porcentaje = 0
    palabra = ""

    # Read each line of the body
    for linea in cuerpo:

      # Split the string by spaces
      sub_string = list( filter( None, re.split("\s{1,}", linea) ) )

      # Check if it starts with a number
      match = re.search("\d", linea)

      # If it does it is a new line
      if match:
        
        # Save the old line
        if palabra != "":
          nueva_fila = pandas.DataFrame([[cluster, cantidad, porcentaje, palabra]], columns = cabecera)
          data_frame = pandas.concat([data_frame, nueva_fila])

        # Build the new line
        cluster = int(sub_string[0])
        cantidad = int(sub_string[1])
        porcentaje = float(sub_string[2].replace(',', '.'))
        palabra = ""
        for i in range( 4, len(sub_string) ):
          palabra = palabra + sub_string[i] + " "
      
      # If it doesn't it is the same line
      else:

        # Keep building the words
        for i in range( len(sub_string) ):
          palabra = palabra + sub_string[i] + " "

    # Finally, save the last line
    nueva_fila = pandas.DataFrame([[cluster, cantidad, porcentaje, palabra]], columns = cabecera)
    data_frame = pandas.concat([data_frame, nueva_fila])

    return data_frame.head()