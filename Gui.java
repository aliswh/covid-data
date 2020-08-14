import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.Box;
import javax.swing.JFrame;
import javax.swing.JTextArea;

import java.awt.event.KeyEvent;
import java.io.IOException;
import java.awt.AWTException;
import java.awt.Robot;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.time.LocalTime;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import java.io.File;

public class Gui{

  public static void main(String[] args) {

    Path workingDir = Paths.get("..");
    String wk = new String(workingDir.toAbsolutePath().toString());

    String pyPath = Paths.get(wk, "\\Code\\getalldata.py").toString();
    String[] commandsPyPath = {"cmd", "/c", "start", "\"get all data\"", pyPath};
    

    // interface
    JFrame f = new JFrame("Covid-19 Data");
    f.setSize(250, 250);
    f.setLocation(300,200);
    final JTextArea textArea = new JTextArea(10, 40);
    f.getContentPane().add(BorderLayout.CENTER, textArea);

    final JButton button1 = new JButton("Get All Data");
    f.getContentPane().add(button1);
    button1.addActionListener(new ActionListener() {

        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                //  runs cmd
                Runtime.getRuntime().exec(commandsPyPath);
                System.out.println("exec");
        
                } catch (IOException er){
                    er.printStackTrace();
                    }
            textArea.append("\nData downloaded\n");
            LocalTime t = LocalTime.now();
            textArea.append(t.toString());

          /* 
            wait for the .py script to end, so I can open 
            RStudio only when all files are made
                    I scan the tasklist, looking for "py.exe" the process that handles my script
                    While this process exists, keep scanning 
                    only when "py.exe" doesn't exists break the while true loop
           */
            try {
              String line;            // input line to read processes
              String linecheck = "";  // string to append all processes names
              int count = 0;
              while (true) {
                // get all processes names in tasklist.exe
                Process p = Runtime.getRuntime().exec(System.getenv("windir") +"\\system32\\"+"tasklist.exe");
                BufferedReader input =
                      new BufferedReader(new InputStreamReader(p.getInputStream()));
                
                // add all tasklist.exe lines to a String
                while ((line = input.readLine()) != null) {
                  linecheck = linecheck.concat(line);
                  //System.out.println(linecheck);
                  System.out.print("downloading data .  .  .  \r");
                  Thread.sleep(50);
                  System.out.print("downloading data   .  .  .\r");
                } // loop to get all processes names

                // scan the string
                if (linecheck.contains("py.exe") || count == 0) {
                  count++;  // times the py.exe process is counted
                } else { break; } // break the loop when "py.exe" doesn't exist

                linecheck = ""; // clear 
                }
              } catch (Exception err) {
                  err.printStackTrace();
                }
            }
    });

    final JButton button2 = new JButton("Open RStudio");
    f.getContentPane().add(button2);
    button2.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        String[] commands = {"cmd", "/c", "start", "\" Opening RStudio \"","C:\\Program Files\\RStudio\\bin\\rstudio.exe"};
        try {
        Runtime.getRuntime().exec(commands);
        } catch (IOException er){
          er.printStackTrace();
          }
          try {
            //  sleeps to let RStudio open
                Thread.sleep(5000);
        } catch (InterruptedException er) {
                er.printStackTrace();
            }
          try {
            Robot robot = new Robot();
    
            robot.keyPress(KeyEvent.VK_CONTROL);
            robot.keyPress(KeyEvent.VK_SHIFT);
            robot.keyPress(KeyEvent.VK_W);
    
            robot.keyRelease(KeyEvent.VK_W);
            robot.keyRelease(KeyEvent.VK_SHIFT);
            robot.keyRelease(KeyEvent.VK_CONTROL);
        
        } catch (AWTException er) {
                er.printStackTrace();
        }
      }
    });

    final JButton button3 = new JButton("Source Files");
    f.getContentPane().add(button3);
    button3.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        ExecCommands();
      }
    });
    
    
    Box box = Box.createVerticalBox();
    box.add(button1);
    box.add(button2);
    box.add(button3);
    f.add(box);  
  
    f.setVisible(true);
  }

  static void ExecCommands(){
    Path workingDir = Paths.get("..");
    String wk = new String(workingDir.toAbsolutePath().toString());

    String[] arr = new String[0]; 
    String filename = "C:\\Users\\alice\\Desktop\\Tesi\\File\\R PROJECT\\R PROJECT\\R0-master\\data\\zones_list";
    
    try {
      Scanner s = new Scanner(new File(filename));
      List<String> lines = new ArrayList<String>(); 
      while (s.hasNextLine()) { 
        lines.add(s.nextLine()); 
      }
      arr = lines.toArray(new String[0]); 
      } catch (IOException e) {
        e.printStackTrace();}

    for(int i=0; i<arr.length; i++) {
      String path = Paths.get(wk, "\\Data\\" + arr[i] + ".2020.R").toString();
      String[] commands = {"cmd", "/c", "start", "\" loading \"", path};
        
      try {
      //  runs cmd
      Runtime.getRuntime().exec(commands);
      System.out.println(arr[i]);

        try {
        // sleeps to let the file source
          Thread.sleep(1000);
        } catch (InterruptedException e) {
          e.printStackTrace();} 

      } catch (IOException e){
          e.printStackTrace();
          }

      /*
      *   presses the shortcut CTRL+SHIFT+S - Source 
      */
      try {
          Robot robot = new Robot();

          robot.keyPress(KeyEvent.VK_CONTROL);
          robot.keyPress(KeyEvent.VK_SHIFT);
          robot.keyPress(KeyEvent.VK_S);

          robot.keyRelease(KeyEvent.VK_S);
          robot.keyRelease(KeyEvent.VK_SHIFT);
          robot.keyRelease(KeyEvent.VK_CONTROL);
      
      } catch (AWTException e) {
              e.printStackTrace();
    }}
}

}