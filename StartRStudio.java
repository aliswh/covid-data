import java.awt.event.KeyEvent;
import java.io.IOException;
import java.awt.AWTException;
import java.awt.Robot;

class StartRStudio {
    public static void main(String args[])
        throws IOException
    {
        /*
        *  file .R da aprire
        *  (to add more: they need to be formatted with two backslashes '\\' instead of one '\')
        */
        String percorsoEst = new String("C:\\Users\\alice\\Desktop\\Tesi\\File\\R PROJECT\\R PROJECT\\R0-master\\R\\est.R0.TD.R");
        //percorsoEst = new String(YOUR PATH HERE);
        String percorsoItaly2020 = new String("C:\\Users\\alice\\Desktop\\Tesi\\File\\R PROJECT\\R PROJECT\\R0-master\\data\\Italy.2020.R");
        //percorsoItaly2020 = new String(YOUR PATH HERE);
        String pyPath = new String("C:\\Users\\alice\\Desktop\\Tesi\\Code\\makeFile.py");
        //pyPath = new String(YOUR PATH HERE);
        
        /*
        *  command line to execute in cmd
        *  (one for each file)
        */
        String[] commandsEst = {"cmd", "/c", "start", "\"commandsEst\"", percorsoEst};
        String[] commandsItaly = {"cmd", "/c", "start", "\"commandsItaly\"", percorsoItaly2020};
        String[] commandsPyPath = {"cmd", "/c", "start", "\"commandsPyPath\"", pyPath};

        /*
        *  command execution:
        *  first gets the daily data by the .py script, then opens RStudio
        */
        Runtime.getRuntime().exec(commandsPyPath);

        ExecCommands(commandsItaly);
        ExecCommands(commandsEst);
    }

    static void ExecCommands(String[] c){
        try {
        //  runs cmd
        Runtime.getRuntime().exec(c);
        } catch (IOException e){
            e.printStackTrace();
        }

        try {
        //  sleeps to let RStudio open
            Thread.sleep(6000);
        } catch (InterruptedException e) {
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
        }
    }
    
}