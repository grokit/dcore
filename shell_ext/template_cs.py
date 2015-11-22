import sys

_meta_shell_command = 'template_cs'

template = """
//Compile: `gmcs file.cs`.

public class HelloWorld
{
        static public void Main ()
            {
                Console.WriteLine ("Hello Mono World");
            }
}
"""

if __name__ == '__main__':
    name = 'code.cs'

    if len(sys.argv) > 1:
        name = sys.argv[1]

    open(name, 'w').write(template)
