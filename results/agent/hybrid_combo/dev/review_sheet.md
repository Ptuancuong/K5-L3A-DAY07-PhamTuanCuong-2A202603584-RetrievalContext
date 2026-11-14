# Review sheet: hybrid_combo / dev

## d01 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is a single 1 or 0 stored inside a computer called?
- Expected: A binary digit, or bit.
- Queries: ['What is a single 1 or 0 stored inside a computer called?']
- Answer: A single 1 or 0 is called a binary digit, or bit. [B:openstax-intro-cs:p205:c1]
- Citations: ['B:openstax-intro-cs:p205:c1']

## d02 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What term is used for the internal design of the processor?
- Expected: Microarchitecture.
- Queries: ['What term is used for the internal design of the processor?']
- Answer: The internal design of the processor is called its microarchitecture: "The architecture (i.e., design) of the microprocessor (i.e., the processor) is called microarchitecture" [B:openstax-intro-cs:p213:c0].
- Citations: ['B:openstax-intro-cs:p213:c0']

## d03 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In IEEE 754 double precision, what value is subtracted from the exponent?
- Expected: 1023 (for single precision it is 127).
- Queries: ['In IEEE 754 double precision, what value is subtracted from the exponent?']
- Answer: For double precision (64-bit), 1023 is subtracted from the exponent (the bias); this is the "excess" value used instead of 127 for single precision. [B:openstax-intro-cs:p220:c2]
- Citations: ['B:openstax-intro-cs:p220:c2']

## d04 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In the IEEE 754 format, what does it mean when the exponent is all 1s but the fraction is not zero?
- Expected: It is NaN (Not a Number) and raises an exception.
- Queries: ['In the IEEE 754 format, what does it mean when the exponent is all 1s but the fraction is not zero?']
- Answer: When the exponent is all 1s and the fraction is non-zero, the value is NaN (Not a Number), which raises an exception. This typically results from a program bug such as dividing by 0 or taking the square root of -1. [B:openstax-intro-cs:p220:c4]
- Citations: ['B:openstax-intro-cs:p220:c4']

## d05 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: When is the zero flag set to 1 in x86?
- Expected: When the previous instruction has generated 0 as a result.
- Queries: ['When is the zero flag set to 1 in x86?']
- Answer: In x86, the zero flag is set to 1 when the previous instruction generated 0 as a result, for example when subtracting two registers gives a result of 0 [B:openstax-intro-cs:p226:c4]. The jump-if-equal (je) instruction jumps when the zero flag is set to 1 [B:openstax-intro-cs:p226:c4].
- Citations: ['B:openstax-intro-cs:p226:c4']

## d06 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is it called when the processor looks for data in the cache and the cache does not have it?
- Expected: A cache miss.
- Queries: ['What is it called when the processor looks for data in the cache and the cache does not have it?']
- Answer: When the processor asks the cache for data and the cache does not have it, this is called a cache miss [B:openstax-intro-cs:p232:c3]. (The opposite, when the data is found in the cache, is a cache hit.)
- Citations: ['B:openstax-intro-cs:p232:c3']

## d07 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: How fast are sequential reads and writes on an SSD?
- Expected: Sequential read reaches 7000 MB/s and sequential write reaches 5000 MB/s.
- Queries: ['How fast are sequential reads and writes on an SSD?']
- Answer: According to the text, an SSD's sequential read reaches 7000 MB/s and its sequential write reaches 5000 MB/s. Random access has lower speed for both reads and writes. [B:openstax-intro-cs:p234:c1]
- Citations: ['B:openstax-intro-cs:p234:c1']

## d08 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is the bootstrap code?
- Expected: A privileged system program; the first code executed when the OS starts.
- Queries: ['What is the bootstrap code?']
- Answer: The bootstrap code is a privileged system program that can run only in kernel mode; it is the first code executed when the OS starts, and the OS depends on it being loaded to work correctly [B:openstax-intro-cs:p262:c2].
- Citations: ['B:openstax-intro-cs:p262:c2']

## d09 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What was the first example of a layered operating system design and when was it designed?
- Expected: Dijkstra's THE system, designed in 1968.
- Queries: ['What was the first example of a layered operating system design and when was it designed?']
- Answer: The first example of a layered approach was Dijkstra's THE system, designed in 1968. It had six layers (0 to 5), from hardware at the bottom up to the job manager that executes users' programs. [B:openstax-intro-cs:p264:c0]
- Citations: ['B:openstax-intro-cs:p264:c0']

## d10 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is the name for moving the CPU from running one process to running another?
- Expected: A context switch.
- Queries: ['What is the name for moving the CPU from running one process to running another?']
- Answer: The act of switching the CPU from one process to another is called a context switch [B:openstax-intro-cs:p273:c5].
- Citations: ['B:openstax-intro-cs:p273:c5']

## d11 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What problem occurs when memory blocks are too small to be given to processes and stay unused?
- Expected: Fragmentation.
- Queries: ['What problem occurs when memory blocks are too small to be given to processes and stay unused?']
- Answer: This problem is fragmentation. When memory blocks are too small to be allocated to processes and remain unused, it is called fragmentation; the source distinguishes internal fragmentation (a block larger than the process leaves part unused) and external fragmentation (enough total space exists but is not contiguous) [B:openstax-intro-cs:p279:c1].
- Citations: ['B:openstax-intro-cs:p279:c1']

## d12 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What happens when the CPU requests a page that is not in main memory?
- Expected: A page fault occurs.
- Queries: ['What happens when the CPU requests a page that is not in main memory?']
- Answer: When the CPU demands a page that is not present in main memory, this is a page fault. The CPU transfers control from the program to the OS, which finds a free page frame in memory, loads the page from the backing store into main memory, and resumes execution of the thread; the CPU has special hardware to help resume execution after the page fault [B:openstax-intro-cs:p283:c0].
- Citations: ['B:openstax-intro-cs:p283:c0']

## d13 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Which encoding was approved in 1963 and later revised several times, and in which years was it revised?
- Expected: ASCII; approved in 1963 and revised in 1965, 1967, 1968, 1977 and 1986.
- Queries: ['Which encoding was approved in 1963 and later revised several times, and in which years was it revised?']
- Answer: The encoding is ASCII (American Standard Code for Information Interchange), approved in 1963 and then revised in 1965, 1967, 1968, 1977, and 1986 [B:openstax-intro-cs:p218:c2].
- Citations: ['B:openstax-intro-cs:p218:c2']

## d14 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What technique does the operating system use to keep programs from overwriting each other's data, and what is it called?
- Expected: Virtual memory: the OS isolates programs so they do not overwrite each other's data or corrupt each other's files.
- Queries: ["What technique does the operating system use to keep programs from overwriting each other's data, and what is it called?"]
- Answer: The OS uses a technique called virtual memory to isolate different programs from each other so that they do not overwrite each other's data or corrupt each other's files [B:openstax-intro-cs:p214:c1].
- Citations: ['B:openstax-intro-cs:p214:c1']

## d15 (answerable) | status=answered | searches=1 | context_hit=False | cited_gold_chunk=False
- Q: What does scheduling mean?
- Expected: Choosing which process to run next (removing the running process from the CPU and selecting another one according to a strategy).
- Queries: ['What does scheduling mean?']
- Answer: Scheduling is the act of determining which process is in the ready state and should be moved to the running state when more resources are requested than can be granted immediately, and in which order such requests should be serviced. Examples include processor scheduling (one processor, many threads) and memory scheduling in virtual memory systems [B:openstax-intro-cs:p274:c0].
- Citations: ['B:openstax-intro-cs:p274:c0']

## d16 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: According to Moore's law, how often would the number of devices inside the processor double?
- Expected: Every 18 months (Gordon Moore's 1965 prediction).
- Queries: ["According to Moore's law, how often would the number of devices inside the processor double?"]
- Answer: According to Moore's law, the number of devices inside the processor would double every 18 months [B:openstax-intro-cs:p236:c4].
- Citations: ['B:openstax-intro-cs:p236:c4']

## d17 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is Intel's name for simultaneous multithreading?
- Expected: Hyperthreading technology.
- Queries: ["What is Intel's name for simultaneous multithreading?"]
- Answer: Intel calls simultaneous multithreading (SMT) "hyperthreading technology." [B:openstax-intro-cs:p238:c1]
- Citations: ['B:openstax-intro-cs:p238:c1']

## d18 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What does a journaling file system do?
- Expected: It records the changes in a separate log file, sometimes called a journal file.
- Queries: ['What does a journaling file system do?']
- Answer: A journaling file system uses write-ahead logging: it records the changes to information in a separate log file (called a journal) prior to any new change or update on the system. [B:openstax-intro-cs:p292:c1]
- Citations: ['B:openstax-intro-cs:p292:c1']

## d19 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: How does the storage access latency of disks compare with that of flash memory?
- Expected: About 10 ms for disks versus about 100 µs for flash memory.
- Queries: ['How does the storage access latency of disks compare with that of flash memory?']
- Answer: Disks have a storage access latency of around 10 ms, while flash memory's is around 100 µs, so flash is roughly 100 times lower latency than disks. [B:openstax-intro-cs:p293:c2]
- Citations: ['B:openstax-intro-cs:p293:c2']

## d20 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Why are SSDs faster and more durable than hard disk drives?
- Expected: SSDs have no moving/mechanical parts (unlike HDDs with rotating disks and read/write heads), which increases durability and makes reads and writes much faster.
- Queries: ['Why are SSDs faster and more durable than hard disk drives?']
- Answer: SSDs have no moving parts, unlike HDDs with rotating disks and read/write heads; this makes them more durable (no parts to wear out or fail, better resistance to drops and impacts) and lets data be read/written faster. Flash memory also allows random access, so scattered data is read quicker than with HDDs, which must physically move the head, and SSDs have lower latency because no head needs positioning [B:openstax-intro-cs:p288:c3][B:openstax-intro-cs:p288:c4].
- Citations: ['B:openstax-intro-cs:p288:c3', 'B:openstax-intro-cs:p288:c4']

## d21 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is a thread?
- Expected: A path of execution within a process (a basic unit of execution); a process may contain multiple threads that share its resources.
- Queries: ['What is a thread?']
- Answer: A thread is the OS's unit of concurrency and the abstraction of a virtual CPU core: a basic unit of execution that runs a set of instructions in a specific order. It is a lightweight process that shares OS resources (such as memory and I/O) with other threads in the same process [B:openstax-intro-cs:p271:c1].
- Citations: ['B:openstax-intro-cs:p271:c1']

## d22 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What do we call the group of wires that links the CPU, the memory and the graphics card so they can exchange data?
- Expected: A bus (a collection of wires that transfers data between the components).
- Queries: ['What do we call the group of wires that links the CPU, the memory and the graphics card so they can exchange data?']
- Answer: The group of wires is called a bus. The passage states that the CPU, memory and graphics card are connected via a collection of wires referred to as a bus, whose purpose is to transfer data between the pieces of the computer [B:openstax-intro-cs:p207:c0].
- Citations: ['B:openstax-intro-cs:p207:c0']

## d23 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In one's complement representation, how can you tell that a binary number is negative?
- Expected: If the most significant bit is 1, the number is negative (it is stored in one's complement form; taking the one's complement again gives the original magnitude).
- Queries: ["In one's complement representation, how can you tell that a binary number is negative?"]
- Answer: In one's complement, look at the most significant bit: if it is 1, the number is negative and is stored in its one's complement form (you must take the one's complement again to find its original value). If it is 0, the number is positive and is read as unsigned. [B:openstax-intro-cs:p216:c4]
- Citations: ['B:openstax-intro-cs:p216:c4']

## d24 (answerable) | status=answered | searches=2 | context_hit=True | cited_gold_chunk=True
- Q: In operating system design, which concept decides what should be done and which concept carries out how it is done?
- Expected: A policy decides what needs to be done; a mechanism is the activity that enforces the policy (how to do it).
- Queries: ['In operating system design, which concept decides what should be done and which concept carries out how it is done?', 'policy versus mechanism operating system design separation']
- Answer: A policy decides what needs to be done (choosing which activities to perform), and a mechanism carries out how it is done (the activity that enforces the policy). [B:openstax-intro-cs:p253:c0]
- Citations: ['B:openstax-intro-cs:p253:c0']

## d25 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Which piece of software lets one physical server host several guest operating systems by creating and managing virtual machines?
- Expected: A hypervisor (virtual machine monitor, VMM).
- Queries: ['Which piece of software lets one physical server host several guest operating systems by creating and managing virtual machines?']
- Answer: A hypervisor (also called a virtual machine monitor, or VMM) is the software layer that sits between the server's hardware and its operating systems, and it creates and manages the virtual machines that run the guest operating systems [B:openstax-intro-cs:p253:c2].
- Citations: ['B:openstax-intro-cs:p253:c2', 'B:openstax-intro-cs:p293:c5']

## d26 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: On a UNIX-like system, where is the mapping from a file's name to its inode kept?
- Expected: In directories, which are special files listing file names and their corresponding inodes (the inode itself does not contain the name).
- Queries: ["On a UNIX-like system, where is the mapping from a file's name to its inode kept?"]
- Answer: On a UNIX-like system, the name-to-inode mapping is stored in directories. Directories are special files that list names of files and their corresponding inodes [B:openstax-intro-cs:p285:c3]. Directories are stored on disk like regular files, with each containing <name, address> pairs [B:openstax-intro-cs:p284:c3].
- Citations: ['B:openstax-intro-cs:p285:c3', 'B:openstax-intro-cs:p284:c3']

## ud01 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: What is the maximum file size supported by the FAT32 file system?
- Expected: The corpus only describes FAT as a table mapping file names to clusters (p285); it never mentions FAT32 or any file size limit.
- Queries: ['What is the maximum file size supported by the FAT32 file system?', 'FAT32 maximum file size 4 GB limit', 'FAT32 file system maximum file size']
- Answer: The retrieved passages do not state the maximum file size supported by FAT32. They only describe FAT as a table mapping files to disk clusters, without giving any size limit.
- Citations: []

## ud02 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: How many transistors does Intel's Core i9 processor contain?
- Expected: The corpus only says generally that a single processor contains billions of transistors (p213); no specific Intel Core i9 figure exists.
- Queries: ["How many transistors does Intel's Core i9 processor contain?", 'Core i9 transistor count billion', 'Intel Core i9 processor transistors']
- Answer: The passages do not state how many transistors Intel's Core i9 processor contains. They only describe transistors generally and Moore's law. Insufficient evidence.
- Citations: []

## ud03 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: Which page replacement algorithm does Windows 11 use?
- Expected: Page replacement is defined generically (p283) but no algorithm per OS and no Windows 11 are mentioned.
- Queries: ['Which page replacement algorithm does Windows 11 use?', 'Windows page replacement algorithm clock least recently used', 'Windows 11 memory management']
- Answer: The passages do not say which page replacement algorithm Windows 11 uses. They only describe page replacement in general terms: when memory is full, one page is swapped to disk to make room for the requested page [B:openstax-intro-cs:p283:c2]. Windows 11 is not mentioned.
- Citations: []
