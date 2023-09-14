import phase1, phase2
import re


understand = phase1.run('./example-2/src/index.js')

print("The manager understands the code the following way:\n"+understand+"\n---------------------------------\n")

generate = phase2.run(understand)

print("The following code is generated:\n"+generate+"\n-----------------------------\n")

index_ts_file = "./flow/index.ts"

pattern = r"```typescript(.*?)```"
matches = re.findall(pattern, generate, re.DOTALL)


# parsing
if matches:
    generate_parsed = matches[0]
    
else:
    print("This is bad.")


with open(index_ts_file, "w") as ts_file:
    ts_file.write(generate_parsed)

print("index.ts file created... about to run...")



# Run the ts file

#import subprocess


#typescript_file = "flow/index.ts"

#try:
#    #Use subprocess to run the "tsc" command
#    subprocess.check_call(["tsc", typescript_file])
#except subprocess.CalledProcessError as e:
#    print(f"TypeScript compilation error: {e}")
#except FileNotFoundError:
#    print("TypeScript compiler (tsc) not found. Make sure it's installed and in your system's PATH.")
