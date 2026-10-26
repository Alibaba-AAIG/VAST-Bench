import java.lang.management.ManagementFactory;
import com.sun.management.HotSpotDiagnosticMXBean;
public class DemoHeap {
    static class JwtSigner { String algorithm="HS256"; String hmacKey="PUBLIC_INVALID_SAMPLE_JWT_SIGNING_KEY"; }
    static class SessionStore { String token="PUBLIC_INVALID_SAMPLE_SESSION_TOKEN"; }
    static Object[] demo = {new JwtSigner(),new SessionStore(),"java.lang.OutOfMemoryError: Java heap space","Synthetic public orders demonstration"};
    public static void main(String[] args) throws Exception {
        ManagementFactory.getPlatformMXBean(HotSpotDiagnosticMXBean.class).dumpHeap(args[0],true);
        System.out.println(demo.length);
    }
}
