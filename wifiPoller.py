#file  -- wifiPoller.py --
import threading
import sys
import subprocess
import time


interface = "wlan0"

class wifiPoller(threading.Thread):

  parsed_cells=[]
  running = True

  # You can add or change the functions to parse the properties of each AP (cell)
  # below. They take one argument, the bunch of text describing one cell in iwlist
  # scan and return a property of that cell.
  def __init__(self):
    threading.Thread.__init__(self)
    #self.parsed_cells=[]
    self.running = True 

  # def print_cells(cells):
  #     table=[columns]
  #     for cell in cells:
  #         cell_properties=[]
  #         for column in columns:
  #             cell_properties.append(cell[column])
  #         table.append(cell_properties)
  #     print_table(table)

  def run(self):
    try:
      while self.running:
      
        cells=[[]]
        self.parsed_cells=[]

        proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()

        for line in out.split("\n"):
            cell_line = self.match(line,"Cell ")
            if cell_line != None:
                cells.append([])
                line = cell_line[-27:]
            cells[-1].append(line.rstrip())

        cells=cells[1:]
        #print cells

        for cell in cells:
            self.parsed_cells.append(self.parse_cell(cell))


        #sort_cells(parsed_cells)
        #print_cells(self.parsed_cells)
        time.sleep(1) # tune this, you might not get values that quickly


        #self.running = false;
    except StopIteration:
      pass

  def inWifiRange(self, bssid,quality):
    try:
      # scan through 
      print bssid 
      signalQ = None
      for cell in self.parsed_cells:
        
        if cell['Address'] == bssid:
          print "wifi ", cell['Address'], ": ", cell['Name']," is in range. Signal Quality: ", cell['Quality'], "%"
          signalQ = cell['Quality']
          break
        else:
          #print "not in range"
          signalQ = 0

      if(signalQ>quality):
        return True
      else:
        return False
    except StopIteration:
      pass


  def get_name(self, cell):
      return self.matching_line(cell,"ESSID:")[1:-1]

  def get_quality(self, cell):
      quality = self.matching_line(cell,"Quality=").split()[0].split('/')
      #return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"
      return int(round(float(quality[0]) / float(quality[1]) * 100))

  def get_address(self, cell):
      return self.matching_line(cell,"Address: ")

  def get_signal_level(self, cell):
      # Signal level is on same line as Quality data so a bit of ugly
      # hacking needed...
      signalString = self.matching_line(cell,"Quality=").split("Signal level=")[1]
      return int(signalString.split(' ')[0])








  def parse_cell(self,cell):
      """Applies the rules to the bunch of text describing a cell and returns the
      corresponding dictionary"""
      parsed_cell={}
      parsed_cell.update({"Address":self.get_address(cell)})
      parsed_cell.update({"Name":self.get_name(cell)})
      parsed_cell.update({"Signal":self.get_signal_level(cell)})
      parsed_cell.update({"Quality":self.get_quality(cell)})
      
      

      #print parsed_cell
      return parsed_cell
      


  def matching_line(self,lines, keyword):
      """Returns the first matching line in a list of lines. See match()"""
      for line in lines:
          matching=self.match(line,keyword)
          if matching!=None:
              return matching
      return None

  def match(self,line,keyword):
      """If the first part of line (modulo blanks) matches keyword,
      returns the end of that line. Otherwise returns None"""
      line=line.lstrip()
      length=len(keyword)
      if line[:length] == keyword:
          return line[length:]
      else:
          return None



  

"""


def get_encryption(cell):
    enc=""
    if matching_line(cell,"Encryption key:") == "off":
        enc="Open"
    else:
        for line in cell:
            matching = match(line,"IE:")
            if matching!=None:
                wpa2=match(matching,"IEEE 802.11i/WPA2 Version ")
                if wpa2!=None:
                    #enc="WPA2 v."+wpa2
                    enc="WPA2"
                wpa=match(matching,"WPA Version ")
                if wpa!=None:
                    enc="WPA v."+wpa
        if enc=="":
            enc="WEP"
    return enc


def get_channel(cell):
    frequency = matching_line(cell,"Frequency:")
    channel = frequency[frequency.index("(")+9:frequency.index(")")]
    return channel


    def get_signal_level(cell):
    # Signal level is on same line as Quality data so a bit of ugly
    # hacking needed...
    level = matching_line(cell,"Quality=").split("Signal level=")[1]
    level = level.split()[0].split('/')
    return str(int(round(float(level[0]) / float(level[1]) * 100))).rjust(3) + " %"
    """

"""
  def print_table(table):
      widths=map(max,map(lambda l:map(len,l),zip(*table))) #functional magic

      justified_table = []
      for line in table:
          justified_line=[]
          for i,el in enumerate(line):
              justified_line.append(el.ljust(widths[i]+2))
          justified_table.append(justified_line)
      
      for line in justified_table:
          for el in line:
              print el,
          print


"""







