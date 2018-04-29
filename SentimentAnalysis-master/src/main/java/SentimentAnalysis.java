import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class SentimentAnalysis {

    public static class SentimentSplit extends Mapper<Object, Text, Text, IntWritable> {

        public Map<String, String> emotionDic = new HashMap<String, String>();

        @Override
        public void setup(Context context) throws IOException{
            Configuration configuration = context.getConfiguration();
            String dicName = configuration.get("dictionary", "");

            BufferedReader br = new BufferedReader(new FileReader(dicName));
            String line = br.readLine();

            while (line != null) {
                String[] word_feeling = line.split("\t");
                emotionDic.put(word_feeling[0].toLowerCase(), word_feeling[1]);
                line = br.readLine();
            }
            br.close();
        }

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            String fileName = ((FileSplit) context.getInputSplit()).getPath().getName();
            String line = value.toString().trim();
            String[] words = line.split("\\s+");
            for (String word: words) {
                if (emotionDic.containsKey(word.trim().toLowerCase())) {
                    context.write(new Text(fileName + "\t" + emotionDic.get(word.toLowerCase())), new IntWritable(1));
                }
            }

        }
    }

    public static class SentimentCollection extends Reducer<Text, IntWritable, Text, IntWritable> {

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {

            int sum = 0;
            for (IntWritable value: values) {
                sum += value.get();
            }

            context.write(key, new IntWritable(sum));
        }

    }

    public static void main(String[] args) throws Exception {

        Configuration configuration = new Configuration();
        configuration.set("dictionary", args[2]);

        Job job = Job.getInstance(configuration);
        job.setJarByClass(SentimentAnalysis.class);
        job.setMapperClass(SentimentSplit.class);
        job.setReducerClass(SentimentCollection.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.waitForCompletion(true);
    }
}
