provider "google" {
  credentials = "${file("gce-sa-secret.json")}"
  project     = "jump-awake"
  region      = "us-west1"
}

resource "random_id" "instance_id" {
  byte_length = 8
}

resource "google_compute_instance" "default" {
  name         = "nickify-vm-${random_id.instance_id.hex}"
  machine_type = "n1-standard-2"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  // Make sure flask is installed on all new instances for later steps
  metadata_startup_script = "sudo apt-get update; sudo apt-get install -yq build-essential python-pip rsync; sudo pip install pipenv;"

  network_interface {
    network = "default"

    access_config {
      // Include this section to give the VM an external ip address
    }
  }

  metadata {
    sshKeys = "nickwu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "google_compute_firewall" "default" {
  name    = "app-firewall"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }
}

output "ip" {
  value = "${google_compute_instance.default.network_interface.0.access_config.0.nat_ip}"
}
