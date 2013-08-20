package weibo4j.examples.tags;

import java.util.List;

import java.io.*;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Comparator;
import java.util.Collections;
import java.util.ArrayList;

import weibo4j.Tags;
import weibo4j.examples.oauth2.Log;
import weibo4j.model.Tag;
import weibo4j.model.WeiboException;

public class GetTags {

	static class ByValueComparator implements Comparator<String> {
		HashMap<String, Integer> base_map;

		public ByValueComparator(HashMap<String, Integer> base_map) {
			this.base_map = base_map;
		}

		public int compare(String arg0, String arg1) {
			if (!base_map.containsKey(arg0) || !base_map.containsKey(arg1)) {
				return 0;
			}

			if (base_map.get(arg0) < base_map.get(arg1)) {
				return 1;
			} else if (base_map.get(arg0) == base_map.get(arg1)) {
				return 0;
			} else {
				return -1;
			}
		}
	}

	// add by John_Czg1989
	public static Set readFileByLines(String filename){
		Set myIDSet = new HashSet<String>();
		File file = new File(filename);
		BufferedReader reader = null;
		try {
			reader = new BufferedReader(new FileReader(file));
			String tempString = null;
			tempString = reader.readLine();
			while((tempString = reader.readLine()) != null)
			{
				String[] mylist = tempString.split("\3");
				myIDSet.add(mylist[0]);
			}
		} catch (IOException e) {
			// TODO: handle exception
			e.printStackTrace();
		}finally{
			if(reader != null){
				try {
					reader.close();
				} catch (IOException e1) {
					// TODO: handle exception
				}
			}
		}
		return myIDSet;
	}
	
	//获取目录下包括该目录下子目录中的所有文件
	static Set myFilePath = new HashSet<String>();
	public static void getAllFile(String dir){
		File myFile = new File(dir);
		File[] files = myFile.listFiles();
		for(int i = 0; i < files.length; ++i)
		{
			if(!files[i].isDirectory()){
				String path = files[i].getAbsolutePath();
				if (path.indexOf("用户.txt") != -1) {
					myFilePath.add(path);
				}
			}
			else {
				getAllFile(files[i].getAbsolutePath());
			}
		}
	}
	public static void main(String[] args) throws IOException {
		
		String access_token ="";
		Tags tm = new Tags();
		tm.client.setToken(access_token);
		
		String dir = "C:\\Users\\Topman3758\\Desktop\\ntt_data\\ntt_data\\ntt";
		//readFileByLines1(dir+"\\现代胜达\\用户标签.txt");
		getAllFile(dir);
		Iterator<String> it = myFilePath.iterator();;
		while(it.hasNext()){
			String filepath = it.next();
			System.out.println(filepath);
			Set myIDSet = readFileByLines(filepath);
			filepath = filepath.substring(0, filepath.lastIndexOf('\\')+1);
			String writepath = filepath;
			writepath += "用户标签.txt";
			System.out.println(writepath+"!!!!");
			FileWriter fWriter = new FileWriter(writepath);
			Iterator<String> it_id = myIDSet.iterator();
			HashMap<String, Integer> mymap = new HashMap<String, Integer>();
			while (it_id.hasNext()) {
				String uid = it_id.next();
				List<Tag> tagsList = null;
				try {
					tagsList = tm.getTags(uid);
					String labelString = "";
					int i = 0;
					if(tagsList.isEmpty())
						continue;
					for(Tag tag:tagsList){				
						//Log.logInfo(tag.toString());
						//System.out.println(tag.toString()+"!!!");
						String tagString = tag.toString();
						String mystr = tagString.substring(tagString.indexOf('[')+1, tagString.indexOf(']'));
						if(mystr.compareTo("") == 0)
							continue;
						//String[] arrStrings = tag.toString().split(" ");
						String[] values = mystr.split(", ");
						if(i != 0)
							labelString = labelString.concat("\3");
						String label = values[1].substring(values[1].indexOf('=')+1);
						if(mymap.containsKey(label))
							mymap.put(label, Integer.valueOf(mymap.get(label).intValue()+1));
						else {
							mymap.put(label, Integer.valueOf(1));
						}
						labelString = labelString.concat(label);
						labelString = labelString.concat(":");
						labelString = labelString.concat(values[2].substring(values[2].indexOf('=')+1));
						++i;
						//System.out.println("####"+labelString);
					}
					fWriter.write(uid+'\3'+labelString+"\n");
				} catch (WeiboException e) {
					e.printStackTrace();
				}
			}
			fWriter.flush();
			fWriter.close();
			ByValueComparator bvc = new ByValueComparator(mymap);
			List<String> keys = new ArrayList<String>(mymap.keySet());
			Collections.sort(keys, bvc);
			int num = 0;
			FileWriter fw = new FileWriter(filepath + "top100.txt");
			for(String key : keys) {
				System.out.printf("%s -> %d\n", key, mymap.get(key));
				String content = key + " -> " + mymap.get(key);
				fw.write(content+"\n");
				if(num > 100)
					break;
				++num;
			}
			fw.flush();
			fw.close();
			System.out.println("filesize = " + myIDSet.size());
		}
	}
}
