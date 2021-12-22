import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfDMatch;
import org.opencv.core.MatOfFloat;
import org.opencv.core.MatOfKeyPoint;
import org.opencv.features2d.AKAZE;
import org.opencv.features2d.BFMatcher;
import org.opencv.features2d.Features2d;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

class testAKAZE{
  public static void main(String[] args) {
    System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    
    Mat img1 = Imgcodecs.imread("data/IMG_Right.jpg");
    Mat img2 = Imgcodecs.imread("data/TestData2.png");
    
    Mat gray1 = new Mat();
    Mat gray2 = new Mat();
    
    Imgproc.cvtColor(img1, gray1, Imgproc.COLOR_BGR2GRAY);
    Imgproc.cvtColor(img2, gray2, Imgproc.COLOR_BGR2GRAY);
    
    AKAZE akaze = AKAZE.create();
    
    MatOfKeyPoint mkp1 = new MatOfKeyPoint();
    MatOfKeyPoint mkp2 = new MatOfKeyPoint();
    
    MatOfFloat des1 = new MatOfFloat();
    MatOfFloat des2 = new MatOfFloat();
    
    Mat mask1 = new Mat();
    Mat mask2 = new Mat();
    
    akaze.detectAndCompute(gray1, mask1, mkp1, des1);
    akaze.detectAndCompute(gray2, mask2, mkp2, des2);
    
    BFMatcher bf = new BFMatcher(Core.NORM_HAMMING,true);
    MatOfDMatch match = new MatOfDMatch();
    
    bf.match(des1, des2, match);
    Mat out = new Mat();
    Features2d.drawMatches(img1, mkp1, img2, mkp2, match, out);
    Imgcodecs.imwrite("data/out.png",out);
  }
}