import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.FileWriter; 
import java.io.File;
import java.io.BufferedWriter;

import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
//import org.eclipse.jdt.internal.corext.dom.ASTFlattener;
 
public class Get_AST {
    public static CompilationUnit getCompilationUnit(String javaFilePath){
        byte[] input = null;
		try {
		    BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream(javaFilePath));
		    input = new byte[bufferedInputStream.available()];
	            bufferedInputStream.read(input);
	            bufferedInputStream.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();	
		} catch (IOException e) {
			e.printStackTrace();
		}
 
        
		ASTParser astParser = ASTParser.newParser(AST.JLS3);
        astParser.setSource(new String(input).toCharArray());
        astParser.setKind(ASTParser.K_COMPILATION_UNIT);
 
        CompilationUnit result = (CompilationUnit) (astParser.createAST(null));
        
        return result;
    }
    
    public static void main(String[] args) {
    	try {
    		String file_path = ".\\input\\input.java";
    		File output_file = new File(".\\output\\output_1.txt");
    		output_file.createNewFile();
    		CompilationUnit AST_TREE = Get_AST.getCompilationUnit(file_path);
    		System.out.println(AST_TREE);
    		//String output = ASTFlattener.asString(AST_TREE);
    		BufferedWriter out = new BufferedWriter(new FileWriter(output_file));
    		out.write(output);
    		out.close();
    	} catch (Exception e) {
			e.printStackTrace();
		}
  	
    }
}
