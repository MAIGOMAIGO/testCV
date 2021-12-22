import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfDouble;
import org.opencv.core.MatOfRect;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.HOGDescriptor;
import org.opencv.videoio.VideoCapture;

public class findHuman{
  public static void main(String[] args) {
    System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    VideoCapture capture = new VideoCapture();
    capture.open(0);
    
    Mat img = new Mat();
    Mat gray = new Mat();
    
    //HOGの設定
    HOGDescriptor hog = new HOGDescriptor();
    hog.setSVMDetector(HOGDescriptor.getDefaultPeopleDetector());

    MatOfRect mor = new MatOfRect();
    MatOfDouble mod = new MatOfDouble();
    
    //BGRだった
    Scalar colar = new Scalar(0, 0, 255);
    int z=0;
    
    while(true) {
      if(capture.isOpened()) {
        capture.read(img);
        if( !img.empty() ){
          //グレーに変換
          Imgproc.cvtColor(img, gray, Imgproc.COLOR_BGR2GRAY);

          //Rectだけ使用する
          hog.detectMultiScale(gray,mor,mod);
          if(!mor.empty()) {
            for(Rect rect : mor.toArray()) {
              Mat mat = new Mat(img,rect);
//              Imgcodecs.imwrite("data/test"+z+".png",mat);
              //元画像、枠の位置、枠の色、枠の幅
              Imgproc.rectangle(img, rect, colar, 1);
            }
            Imgcodecs.imwrite("data/test"+z+".png",img);
            z++;

            if(z >= 100) {
              System.exit(0);
            }
          }
        }
      }
    }
  }
}