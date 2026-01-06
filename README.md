![](https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/128x128/bf65e024aee34c3cce4bb71e2dce9fc1) 
## Universidad Europea de Andalucía
Máster Universitario en Análisis de Grandes Cantidades de Datos (Big Data)

Estudiante: Boris Paternina Pérez

Tarea 1 - Computación en Sistemas Distribuídos

## Apache Hadoop, HDFS y MapReduce
### Desarrollo y ejecución de un ejercicio básico de WordCount sobre un fichero de 1 GB:
Este ejercicio se desarrolló en una distribución Ubuntu 24.04 LTS bajo wsl2, y java development kit OpenJDK 64-Bit version 1.8.0_472. Las intrucciones para la instalación y configuración de Hadoop y YARN en modo de operación pseudo-distribuída, fueron tomadas de [Hadoop: Setting up a Single Node Cluster.](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SingleCluster.html) 

Adicional a estas instrucciones, se establecieron las siguientes variables en el archivo `.bashrc`:
```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/home/hadoop/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
# variables adicionales para compilar WordCount
export PATH=${JAVA_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=$JAVA_HOME/lib/tools.jar
```
Se estableció la siguiente configuración en el archivo `$HADOOP_HOME/etc/hadoop/core-site.xml` :
```bash
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

Y se estableció la siguiente configuración en el archivo `$HADOOP_HOME/etc/hadoop/hdfs-site.xml` :
```bash
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/hadoop/hadoopdata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/hadoop/hadoopdata/hdfs/datanode</value>
    </property>
 </configuration>
```
Se comprobó la correcta instalación mediante los siguientes comandos:

```bash
ssh localhost
start-dfs.sh
start-yarn.sh
jps
```
Comprobado que están activos los procesos de OpenSSH, Hadoop y YARN, y el clúster HDFS se inició correctamente, procedemos a ejecutar el ejercicio de WordCount.
#### 1. Descarga del archivo [big-quijote.txt](https://objectstorage.eu-paris-1.oraclecloud.com/n/emeasespainsandbox/b/hadoop/o/big-quijote.txt) :
Ejecutamos el siguiente comando dentro del directorio local del proyecto `ueaMasterBD/input/`:
```bash
wget https://objectstorage.eu-paris-1.oraclecloud.com/n/emeasespainsandbox/b/hadoop/o/big-quijote.txt
```
#### 2. Creación del directorio y subida del archivo al clúster HDFS:
Antes de subir el archivo para su análisis en el framework MapReduce, debemos crear el directorio `input`dentro del clúster de HDFS:
```bash
hdfs dfs -mkdir -p /user/hadoop/input
```
Ejecutamos el siguiente comando para subir el archivo big-quijote desde el directorio local del proyecto, hacia el directorio `input`creado anteriormente:
```bash
hdfs dfs -put ueaMasterBD/input/* input
```
#### 3. Creación de la aplicación WordCount:
Se creó el archivo `WordCount.java`dentro del directorio `wordCount/src/`, con el [código suministrado](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Source_Code) en el tutorial MapReduce.

Dentro del directorio `wordCount/src/`, se ejecuta el siguiente comando para crear el archivo `.class`:
```bash
hadoop com.sun.tools.javac.Main WordCount.java
```
Y el siguiente comando para crear el ejecutable `.jar`:
```bash
jar cf wc.jar WordCount*.class
```
El procedimiento descrito en esta sección ha creado los siguientes archivos:
```bash
'WordCount$IntSumReducer.class'
'WordCount$TokenizerMapper.class'
WordCount.class
WordCount.java
wc.jar
```
#### 4. Ejecución de la aplicación WordCount:
- El siguiente comando ejecuta la aplicación `WordCount` sobre todo archivo almacenado en el directorio `input` del clúster HDFS.

- En nuestro caso, creando un archivo con el conteo de todas las palabras presentes en el archivo `big-quijote.txt`.

- La aplicación `WordCount` creará de forma automática el directorio `output` conteniendo el archivo con el conteo:
```bash
hadoop jar wc.jar WordCount /user/hadoop/input /user/hadoop/output
```
Para ver el contenido de `output` ejecutamos el siguiente comando:
```bash
hadoop dfs -ls /user/hadoop/output
```
#### 5. Análisis del resultado de WordCount:
Podemos ejecutar el siguiente comando si queremos ver el resultado generado por la aplicación `WordCount`:
```bash
hdfs dfs -cat /user/hadoop/output/part-r-00000
```
No obstante, el tamaño del archivo (39.755 líneas), no hace práctico su análisis de esta forma.

Por tanto, podemos ejecutar el siguiente script en `bash` que nos permita obtener las 10 palabras más repetidas en el archivo `big-quijote.txt`:
```bash
hdfs dfs -cat /user/hadoop/output/part-00000 | sort -n -r -k2,2 | head
```
El cual nos dá el siguiente resultado:

|   |   |
|---|---|
| que | 10007552 |
| de | 9284096 |
| y | 8179712 |
| la | 5288448 |
| a | 4929024 |
| el | 4100608 |
| en | 4065792 |
| no | 2878464 |
| se | 2432512 |
| los | 2406912 |


