using Microsoft.EntityFrameworkCore;
using Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata;
using System.Text;
using System.Threading.Tasks;

namespace Database
{
    public class MFGContext : DbContext
    {
        public DbSet<UserModel> Users { get; set; }
        public DbSet<FeatureModel> Features { get; set; }
        public DbSet<DeveloperModel> Developers { get; set; }


        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
             => optionsBuilder.UseNpgsql("Host=my_host;Database=my_db;Username=my_user;Password=my_pw");


        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<DeveloperModel>()
                .HasKey(dm => new { dm.DeveloperId, dm.FeatureId });

            modelBuilder.Entity<DeveloperModel>()
                .HasOne(dm => dm.Developer)
                .WithMany(dm => dm.FeaturesDeveloped)
                .HasForeignKey(dm => dm.DeveloperId);

            modelBuilder.Entity<DeveloperModel>()
                .HasOne(dm => dm.Feature)
                .WithMany(dm => dm.Developers)
                .HasForeignKey(dm => dm.FeatureId);
        }

    }
}
